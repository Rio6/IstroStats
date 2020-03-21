from datetime import datetime

import models
from models import PlayerModel, MatchModel, MatchPlayerModel, ServerModel, ServerPlayerModel
from istro_listener import IstroListener

def _isTrue(string):
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

class Istrolid:
    def __init__(self):
        self.fullPlayers = False
        self.fullServers = False

        self.listener = IstroListener(login=True)
        self.listener.on('players', self._onPlayers)
        self.listener.on('playersDiff', self._onPlayersDiff)
        self.listener.on('servers', self._onServers)
        self.listener.on('serversDiff', self._onServersDiff)
        self.listener.on('gameReport', self._onGameReport)
        self.listener.on('close', lambda recon: self.listener.setLogin(not recon))

    def start(self):
        self.listener.connect()

    def stop(self):
        self.listener.close()

    def getPlayerInfo(self, name):
        player = self._getPlayer(name, updateOnline=False)
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

        if _isTrue(_single(query.get('online', ''))):
            rst = rst.filter(PlayerModel.logonTime != None)

        if 'ai' in query:
            rst = rst.filter_by(ai=_isTrue(_single(query['ai'])))

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

        rst = rst.offset(_single(query.get('offset', 0)))
        rst = rst.limit(_single(query.get('limit', 50)))

        return [self._playerToInfo(r) for r in rst]

    def getServers(self, **query):
        rst = models.session.query(ServerModel)

        if 'running' in query:
            if _isTrue(_single(query['running'])):
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
                rst.order_by(ServerModel.runningSince.desc())
            elif order == 'running_asc':
                rst.order_by(ServerModel.runningSince.asc())

        return [self._serverToInfo(r) for r in rst]

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
            rst = rst.filter_by(server=_single(query['server']))

        if 'type' in query:
            rst = rst.filter_by(type=_single(query['type']))

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

        rst = rst.offset(_single(query.get('offset', 0)))
        rst = rst.limit(_single(query.get('limit', 50)))

        return [self._matchToInfo(r) for r in rst]

    def _onPlayers(self, players):
        self.fullPlayers = True
        # update non online players
        (models.session.query(PlayerModel)
                .filter(PlayerModel.name.notin_(players.keys()))
                .update({'logonTime': None, 'mode': None}, synchronize_session='fetch'))
        models.session.commit()
        self._onPlayersDiff(players)
        self._tryLoginless()

    def _onServers(self, servers):
        self.fullServers = True
        # remove non online servers
        models.session.query(ServerModel).filter(ServerModel.name.notin_(servers.keys())).delete(synchronize_session='fetch')
        models.session.commit()
        self._onServersDiff(servers)
        self._tryLoginless()

    def _tryLoginless(self):
        if self.fullPlayers and self.fullServers:
            print("Reconnecting without login")
            self.listener.setLogin(False)
            self.listener.reconnect()

    def _onPlayersDiff(self, diff):
        for name, playerInfo in diff.items():

            if playerInfo is None:
                playerInfo = self._getPlayer(name, create=True)
                playerInfo.lastActive = datetime.utcnow()
                playerInfo.logonTime = None
                playerInfo.mode = None

            else:
                player = self._getPlayer(name, updateOnline=True, create=True)

                player.mode = playerInfo.get('mode', player.mode)
                player.rank = playerInfo.get('rank', player.rank)
                player.faction = playerInfo.get('faction', player.faction)
                if 'color' in playerInfo:
                    player.color = str.format('#{:02x}{:02x}{:02x}{:02x}', *playerInfo['color'])

            models.session.commit()

    def _onServersDiff(self, diff):
        for name, serverInfo in diff.items():
            if serverInfo is None:
                models.session.query(ServerModel).filter_by(name=name).delete(synchronize_session='fetch')
            else:

                server = models.get_or_create(ServerModel, name=name)

                if 'players' in serverInfo:

                    def infos():
                        playerInfos = serverInfo['players']
                        for info in playerInfos:
                            player = self._getPlayer(info['name'], info['ai'], updateOnline=False, create=True)
                            yield (player.id, info)

                    server.players = [ServerPlayerModel(playerId=id, side=info['side']) for id, info in infos()]

                if 'state' in serverInfo:
                    state = serverInfo['state']
                    if state != server.state:
                        if state == 'running':
                            server.runningSince = datetime.utcnow()
                        elif state == 'waiting':
                            server.runningSince = None
                    server.state = state

                server.observers = serverInfo.get('observers', server.observers)
                server.hidden = serverInfo.get('hidden', server.hidden)
                server.type = serverInfo.get('type', server.type)

            models.session.commit()

    def _onGameReport(self, report):
        try:
            match = models.MatchModel(
                server = report['serverName'],
                type = report['type'],
                winningSide = report['winningSide'],
                time = report['time'])

            models.session.add(match)

            for player in report['players']:
                playerId = self._getPlayer(player['name'], player['ai'], create=True).id
                match.players.append(MatchPlayerModel(
                    playerId = playerId,
                    winner = player['side'] == report['winningSide'],
                    side = player['side']))

            models.session.commit()

        except KeyError as e:
            print(e)
            models.session.rollback()

    def _getPlayer(self, name, ai=False, updateOnline=False, create=False):
        if create:
            player = models.get_or_create(PlayerModel, name=name, ai=ai)
        else:
            player = models.session.query(PlayerModel).filter_by(name=name, ai=ai).one_or_none()
            if player is None: return None

        if updateOnline:
            player.lastActive = player.logonTime = datetime.utcnow()

        return player

    def _getPlayerId(self, name, ai=False):
        player = self._getPlayer(name, ai)
        if player is None: return None
        return player.id
