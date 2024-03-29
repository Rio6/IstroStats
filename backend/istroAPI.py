import datetime
import logging

from sqlalchemy.sql.expression import func, or_
from . import models
from .models import PlayerModel, MatchModel, MatchPlayerModel, ServerModel, ServerPlayerModel

# helper functions to ensure we get the right data type from http params
def _bool(string):
    return string.lower() in ('true', 'yes', 't', 'y', '1')

def _single(x):
    if isinstance(x, list):
        return x[0]
    else:
        return x

def _multiple(x):
    if isinstance(x, list):
        return x
    else:
        return [x]

def _clamp(x, a, b=float('inf')):
    return min(max(int(x), a), b)

class IstrolidAPI:

    def report(self, **time):
        lastday = self._parseTime(time, days=1)
        playerCount = models.session.query(PlayerModel).filter(PlayerModel.lastActive > lastday).count()
        gameCount = {
            'total': 0,
            'types': {}
        }

        games = models.session.query(MatchModel).filter(MatchModel.finished > lastday)
        for game in games:
            gameCount['total'] += 1
            gameCount['types'][game.type] = gameCount['types'].get(game.type, 0) + 1

        return {
            'players': playerCount,
            'games': gameCount
        }

    def getPlayers(self, **query):
        rst = models.session.query(PlayerModel)

        if 'name' in query:
            rst = rst.filter(PlayerModel.name.in_(_multiple(query['name'])))

        if 'online' in query:
            if _bool(_single(query['online'])):
                rst = rst.filter(PlayerModel.logonTime != None)
            else:
                rst = rst.filter(PlayerModel.logonTime == None)

        if 'ai' in query:
            rst = rst.filter_by(ai=_bool(_single(query['ai'])))

        if 'search' in query:
            rst = rst.filter(PlayerModel.name.ilike(_single(query['search'])))

        if 'faction' in query:
            factions = _multiple(query['faction'])
            rst = rst.filter(PlayerModel.faction.in_(factions))

        if 'order' in query:
            order = _single(query['order'])
            if order == 'rank_des':
                rst = rst.order_by(PlayerModel.rank.desc(), PlayerModel.id.asc())
            elif order == 'rank_asc':
                rst = rst.order_by(PlayerModel.rank.asc(), PlayerModel.id.asc())
            elif order == 'name_des':
                rst = rst.order_by(PlayerModel.name.desc(), PlayerModel.id.asc())
            elif order == 'name_asc':
                rst = rst.order_by(PlayerModel.name.asc(), PlayerModel.id.asc())
            elif order == 'faction_des':
                rst = rst.order_by(PlayerModel.faction.desc(), PlayerModel.id.asc())
            elif order == 'faction_asc':
                rst = rst.order_by(PlayerModel.faction.asc(), PlayerModel.id.asc())
            elif order == 'logon_des':
                rst = rst.order_by(PlayerModel.logonTime.asc().nullslast(), PlayerModel.lastActive.desc().nullslast(), PlayerModel.id.asc())
            elif order == 'logon_asc':
                rst = rst.order_by(PlayerModel.logonTime.desc().nullsfirst(), PlayerModel.lastActive.asc().nullslast(), PlayerModel.id.asc())

        count = rst.count()

        rst = rst.offset(_clamp(_single(query.get('offset', 0)), 0))
        limit = int(_single(query.get('limit', 50)))
        rst = rst.limit(_clamp(limit, 0, 500))

        return {
            'count': count,
            'players': [self._playerToInfo(r) for r in rst]
        }

    def getServers(self, **query):
        rst = models.session.query(ServerModel)

        if 'name' in query:
            rst = rst.filter_by(name=_single(query['name']))

        if 'running' in query:
            if _bool(_single(query['running'])):
                rst = rst.filter(ServerModel.runningSince != None)
            else:
                rst = rst.filter(ServerModel.runningSince == None)

        if 'type' in query:
            rst = rst.filter_by(type=_single(query['type']))

        if 'player' in query:
            players = _multiple(query['player'])
            rst = (rst.join(ServerPlayerModel).join(PlayerModel)
                    .filter(PlayerModel.name.in_(players)))

        return {
            'servers': [self._serverToInfo(r) for r in rst]
        }

    def getMatches(self, **query):
        rst = models.session.query(MatchModel)

        if 'id' in query:
            try:
                rst = rst.filter_by(id=int(_single(query['id'])))
            except ValueError as e:
                logging.warn("IstroAPI: %s", e);
                rst = rst.where(False)

        if 'player' in query:
            players = _multiple(query['player'])
            rst = (rst.join(MatchPlayerModel).join(PlayerModel)
                    .filter(PlayerModel.name.in_(players)))

        if 'winner' in query:
            winners = _multiple(query['winner'])
            rst = (rst.join(MatchPlayerModel).join(PlayerModel)
                    .filter(PlayerModel.name.in_(winners))
                    .filter(MatchPlayerModel.winner == True))

        if 'loser' in query:
            losers = _multiple(query['loser'])
            rst = (rst.join(MatchPlayerModel).join(PlayerModel)
                    .filter(PlayerModel.name.in_(losers))
                    .filter(MatchPlayerModel.winner == False))

        if 'server' in query:
            rst = rst.filter(or_(MatchModel.server.ilike(search) for search in _multiple(query['server'])))

        if 'type' in query:
            rst = rst.filter(or_(MatchModel.type.ilike(search) for search in _multiple(query['type'])))

        if 'order' in query:
            order = _single(query['order'])
            if order == 'finished_des':
                rst = rst.order_by(MatchModel.finished.desc(), MatchModel.id.asc())
            elif order == 'finished_asc':
                rst = rst.order_by(MatchModel.finished.asc(), MatchModel.id.asc())
            elif order == 'time_des':
                rst = rst.order_by(MatchModel.time.desc(), MatchModel.id.asc())
            elif order == 'time_asc':
                rst = rst.order_by(MatchModel.time.asc(), MatchModel.id.asc())

        count = rst.count()

        rst = rst.offset(_clamp(_single(query.get('offset', 0)), 0))
        limit = int(_single(query.get('limit', 50)))
        rst = rst.limit(_clamp(limit, 0, 500))

        return {
            'count': count,
            'matches': [self._matchToInfo(r) for r in rst]
        }

    def getFactions(self, **query):
        rst = (models.session.query(PlayerModel)
                .with_entities(
                    PlayerModel.faction,
                    func.count(PlayerModel.faction),
                    func.avg(PlayerModel.rank),
                    func.max(PlayerModel.lastActive))
                .filter(PlayerModel.faction != None, PlayerModel.faction != '')
                .group_by(PlayerModel.faction))

        if 'name' in query:
            rst = rst.filter_by(faction=query['name'])

        if 'search' in query:
            rst = rst.filter(PlayerModel.faction.ilike(_single(query['search'])))

        if 'minplayers' in query:
            try:
                rst = rst.having(func.count(PlayerModel.faction) >= int(query['minplayers']))
            except ValueError as e:
                logging.warn("IstroAPI: %s", e);
                rst = rst.where(False)

        if 'order' in query:
            order = _single(query['order'])
            if order == 'playercount_des':
                rst = rst.order_by(func.count(PlayerModel.faction).desc())
            elif order == 'playercount_asc':
                rst = rst.order_by(func.count(PlayerModel.faction).asc())
            elif order == 'name_des':
                rst = rst.order_by(PlayerModel.faction.desc())
            elif order == 'name_asc':
                rst = rst.order_by(PlayerModel.faction.asc())
            elif order == 'rank_des':
                rst = rst.order_by(func.avg(PlayerModel.rank).desc())
            elif order == 'rank_asc':
                rst = rst.order_by(func.avg(PlayerModel.rank).asc())
            elif order == 'active_des':
                rst = rst.order_by(func.max(PlayerModel.lastActive).desc().nullslast())
            elif order == 'active_asc':
                rst = rst.order_by(func.max(PlayerModel.lastActive).asc().nullslast())

        count = rst.count()

        rst = rst.offset(_clamp(_single(query.get('offset', 0)), 0))
        limit = int(_single(query.get('limit', 50)))
        rst = rst.limit(_clamp(limit, 0, 500))


        return {
            'count': count,
            'factions': [{
                'name': r[0],
                'size': r[1],
                'rank': r[2],
                'lastActive': r[3]
            } for r in rst]
        }

    def getPlayerWinRate(self, **query):
        if 'name' not in query:
            return {}

        matchPlayers = (models.session.query(MatchModel, MatchPlayerModel)
            .join(MatchPlayerModel)
            .join(PlayerModel)
            .filter(PlayerModel.name == _single(query['name'])))

        if 'type' in query:
            print(query['type'])
            matchPlayers = matchPlayers.filter(MatchModel.type.in_(_multiple(query['type'])))

        rst = {}
        for match, player in matchPlayers:
            matchRst = rst.setdefault(match.type, {
                'wins': 0,
                'games': 0
            })

            if match.winningSide == player.side:
                matchRst['wins'] += 1

            matchRst['games'] += 1

        return rst

    def getActiveFactions(self, **query):
        after = self._parseTime(query, weeks=4)
        rst = (models.session.query(PlayerModel)
                .with_entities(
                    PlayerModel.faction,
                    func.count(PlayerModel.id),
                    func.max(PlayerModel.lastActive))
                .filter(PlayerModel.faction != None, PlayerModel.faction != '')
                .filter(PlayerModel.lastActive > after)
                .group_by(PlayerModel.faction)
                .order_by(func.count(PlayerModel.id).desc(), func.max(PlayerModel.rank).desc()))

        if 'exclude' in query:
            excludes = _multiple(query['exclude'])
            rst = rst.filter(~PlayerModel.faction.in_(excludes))

        count = rst.count()

        rst = rst.offset(_clamp(_single(query.get('offset', 0)), 0))
        limit = int(_single(query.get('limit', 50)))
        rst = rst.limit(_clamp(limit, 0, 500))

        return {
            'count': count,
            'factions': {r[0]: r[1] for r in rst}
        }

    def _playerToInfo(self, player):
        servers = [rst[0] for rst in (models.session.query(ServerModel.name)
            .join(ServerPlayerModel).filter(ServerPlayerModel.playerId == player.id))]

        return {
            'id': player.id,
            'name': player.name,
            'rank': player.rank,
            'faction': player.faction,
            'color': player.color,
            'mode': player.mode,
            'servers': servers,
            'ai': player.ai,
            'hidden': player.hidden,
            'logonTime': player.logonTime,
            'lastActive': player.lastActive,
        }

    def _serverToInfo(self, server):

        players = []
        for player, serverPlayer in (models.session.query(PlayerModel, ServerPlayerModel)
                .join(PlayerModel).filter(ServerPlayerModel.serverId == server.id)):
            players.append({
                'name': player.name,
                'ai': player.ai,
                'side': serverPlayer.side
            })

        return {
            'name': server.name,
            'players': players,
            'observers': server.observers,
            'type': server.type,
            'state': server.state,
            'hidden': server.hidden,
            'runningSince': server.runningSince
        }

    def _matchToInfo(self, match):

        players = []
        for player, matchPlayer in (models.session.query(PlayerModel, MatchPlayerModel)
                .join(PlayerModel).filter(MatchPlayerModel.matchId == match.id)):
            players.append({
                'name': player.name,
                'ai': player.ai,
                'winner': matchPlayer.winner,
                'side': matchPlayer.side,
            })


        return {
            'id': match.id,
            'server': match.server,
            'finished': match.finished,
            'type': match.type,
            'winningSide': match.winningSide if match.winningSide != '0' else None,
            'time': match.time,
            'players': players
        }

    def _parseTime(self, query, **default):
        try:
            time = datetime.timedelta(
                minutes = float(query.get('minutes', 0)),
                hours   = float(query.get('hours', 0)),
                days    = float(query.get('days', 0)),
                weeks   = float(query.get('weeks', 0)))

            if time.total_seconds() <= 0:
                time = datetime.timedelta(**default)

        except ValueError:
            time = datetime.timedelta(**default)

        return datetime.datetime.utcnow() - time
