import models
from models import PlayerModel, MatchModel, MatchPlayerModel, ServerModel, ServerPlayerModel

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

class IstrolidAPI:

    def getPlayerInfo(self, name):
        player = models.session.query(PlayerModel).filter_by(name=name, ai=False).one_or_none()
        if player is None: return None
        return self._playerToInfo(player)

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
            'logonTime': player.logonTime,
            'lastActive': player.lastActive,
        }

    def getServerInfo(self, name):
        server = models.session.query(ServerModel).filter_by(name=name).one_or_none()
        if server is None: return None
        return self._serverToInfo(server)

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

    def getMatchInfo(self, matchId):
        match = models.session.query(MatchModel).filter_by(id=matchId).one_or_none()
        if match is None: return None
        return self._matchToInfo(match)

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
            'winningSide': match.winningSide,
            'time': match.time,
            'players': players
        }

    def getPlayers(self, **query):
        rst = models.session.query(PlayerModel)

        if 'online' in query:
            if _bool(_single(query['online'])):
                rst = rst.filter(PlayerModel.logonTime != None)
            else:
                rst = rst.filter(PlayerModel.logonTime == None)

        if 'ai' in query:
            rst = rst.filter_by(ai=_bool(_single(query['ai'])))

        if 'search' in query:
            rst = rst.filter(PlayerModel.name.ilike(_single(query['search'])))

        if 'order' in query:
            order = _single(query['order'])
            if order == 'rank_des':
                rst = rst.order_by(PlayerModel.rank.desc())
            elif order == 'rank_asc':
                rst = rst.order_by(PlayerModel.rank.asc())
            elif order == 'name_des':
                rst = rst.order_by(PlayerModel.name.desc())
            elif order == 'name_asc':
                rst = rst.order_by(PlayerModel.name.asc())
            elif order == 'logon_des':
                rst = rst.order_by(PlayerModel.logonTime.asc().nullslast(), PlayerModel.lastActive.desc())
            elif order == 'logon_asc':
                rst = rst.order_by(PlayerModel.logonTime.desc().nullsfirst(), PlayerModel.lastActive.asc())

        count = rst.count()

        rst = rst.offset(_single(query.get('offset', 0)))
        rst = rst.limit(_single(query.get('limit', 50)))

        return {
            'count': count,
            'players': [self._playerToInfo(r) for r in rst]
        }

    def getServers(self, **query):
        rst = models.session.query(ServerModel)

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

        if 'order' in query:
            order = _single(query['order'])
            if order == 'running_des':
                rst = rst.order_by(ServerModel.runningSince.desc().nullsfirst())
            elif order == 'running_asc':
                rst = rst.order_by(ServerModel.runningSince.asc().nullslast())

        return {
            'servers': [self._serverToInfo(r) for r in rst]
        }

    def getMatches(self, **query):
        rst = models.session.query(MatchModel)

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
            rst = rst.filter(MatchModel.server.in_(_multiple(query['server'])))

        if 'type' in query:
            rst = rst.filter(MatchModel.type.in_(_multiple(query['type'])))

        if 'order' in query:
            order = _single(query['order'])
            if order == 'finished_des':
                rst = rst.order_by(MatchModel.finished.desc())
            elif order == 'finished_asc':
                rst = rst.order_by(MatchModel.finished.asc())
            if order == 'time_des':
                rst = rst.order_by(MatchModel.time.desc())
            elif order == 'time_asc':
                rst = rst.order_by(MatchModel.time.asc())

        count = rst.count()

        rst = rst.offset(_single(query.get('offset', 0)))
        rst = rst.limit(_single(query.get('limit', 50)))

        return {
            'count': count,
            'matches': [self._matchToInfo(r) for r in rst]
        }
