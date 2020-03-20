from datetime import datetime

import models
from models import PlayerModel, MatchModel, MatchPlayerModel
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

class Server:
    class Player:
        def __init__(self, name, side, ai=False):
            self.name = name
            self.side = side
            self.ai = ai

    def __init__(self, name):
        self.name = name
        self.players = []
        self.observers = 0
        self.type = None
        self.state = None
        self.hidden = False
        self.runningSince = None

class Istrolid:
    def __init__(self):
        self.onlinePlayers = {}
        self.servers = {}

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
        player = self._getPlayer(name, online=False)

        if player is None: return None

        return {
            'id': player.id,
            'name': player.name,
            'rank': player.rank,
            'faction': player.faction,
            'color': player.color,
            'mode': player.mode,
            'ai': player.ai,
            'logonTime': player.logonTime,
            'lastActive': player.lastActive,
        }

    def getServerInfo(self, name):
        server = self._getServer(name, False)

        if server is None: return None

        return {
            'name': server.name,
            'players': [{
                'name': p.name,
                'side': p.side,
                'ai': p.ai
            } for p in server.players],
            'observers': server.observers,
            'type': server.type,
            'state': server.state,
            'hidden': server.hidden,
            'runningSince': server.runningSince
        }

    def getMatchInfo(self, matchId):
        match = models.session.query(MatchModel).filter_by(id=matchId).one_or_none()

        if match is None: return None

        players = []
        for matchPlayer in models.session.query(MatchPlayerModel).filter_by(matchId=match.id):
            player = models.session.query(PlayerModel).filter_by(id=matchPlayer.playerId).one_or_none()
            if player is not None:
                players.append({
                    'name': player.name,
                    'ai': player.ai,
                    'winner': matchPlayer.winner,
                    'side': matchPlayer.side,
                })


        return {
            'server': match.server,
            'finished': match.finished,
            'type': match.type,
            'winningSide': match.winningSide,
            'time': match.time,
            'players': players
        }

    def getPlayers(self, **query):
        rst = models.session.query(PlayerModel.name)

        if _isTrue(_single(query.get('online', ''))):
            rst = rst.filter(PlayerModel.name.in_([p.name for p in self.onlinePlayers.values()]))

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

        return [self.getPlayerInfo(r[0]) for r in rst]

    def getServers(self, **query):
        rst = []
        for name, server in self.servers.items():
            if 'running' in query:
                if _isTrue(_single(query['running'])) != (server.runningSince is not None):
                    continue

            if 'type' in query:
                if _single(query['type']).lower() != server.type.lower():
                    continue

            if 'player' in query:
                players = _multiple(query['player'])
                if any([p.name not in players for p in server.players]):
                    continue

            rst.append(name)

        return [self.getServerInfo(r) for r in rst]

    def getMatches(self, **query):
        rst = models.session.query(MatchModel.id)

        def matchPlayer(name, winner=None):
            matchPlayer = (models.session.query(MatchPlayerModel)
                    .filter(models.MatchPlayerModel.matchId == models.MatchModel.id))

            playerId = self._getPlayerId(name)
            if playerId is not None:
                matchPlayer = matchPlayer.filter_by(playerId=playerId)
                if winner is not None:
                    matchPlayer = matchPlayer.filter_by(winner=winner)
            else:
                matchPlayer.filter(False)

            return matchPlayer

        if 'player' in query:
            players = _multiple(query['player'])
            for name in players:
                rst = rst.filter(matchPlayer(name).exists())

        if 'winner' in query:
            winners = _multiple(query['winner'])
            for name in winners:
                rst = rst.filter(matchPlayer(name, True).exists())

        if 'loser' in query:
            losers = _multiple(query['loser'])
            for name in losers:
                rst = rst.filter(matchPlayer(name, False).exists())

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

        return [self.getMatchInfo(r[0]) for r in rst]

    def _onPlayers(self, players):
        self.fullPlayers = True
        # filter non existent players
        self.onlinePlayers = {n:p for n,p in self.onlinePlayers.items() if p.name in players}
        self._onPlayersDiff(players)
        self._tryLoginless()

    def _onServers(self, servers):
        self.fullServers = True
        # filter non existent servers
        self.servers = {n:s for n,s in self.servers.items() if s.name in servers}
        self._onServersDiff(servers)
        self._tryLoginless()

    def _tryLoginless(self):
        if self.fullPlayers and self.fullServers:
            print("Reconnecting without login")
            self.listener.setLogin(False)
            self.listener.reconnect()

    def _onPlayersDiff(self, diff):
        for name, player in diff.items():
            if player is None:
                player = self._getPlayer(name, create=True)
                player.lastActive = datetime.utcnow()
                self.onlinePlayers.pop(player.id, None)
            else:
                oldPlayer = self._getPlayer(name, online=True, create=True)

                # database data
                oldPlayer.rank = player.get('rank', oldPlayer.rank)
                oldPlayer.faction = player.get('faction', oldPlayer.faction)
                if 'color' in player:
                    oldPlayer.color = str.format('#{:02x}{:02x}{:02x}{:02x}', *player['color'])
                models.session.commit()

                # in-memory data
                oldPlayer.mode = player.get('mode', oldPlayer.mode)

    def _onServersDiff(self, diff):
        for name, server in diff.items():
            if server is None:
                self.servers.pop(name, None)
            else:
                oldServer = self._getServer(name, True)
                if 'players' in server:
                    oldServer.players = [
                        Server.Player(p.get('name'), p.get('side'), p.get('ai')) for p in server['players']
                    ]

                if 'state' in server:
                    state = server['state']
                    if state != oldServer.state:
                        if state == 'running':
                            oldServer.runningSince = datetime.utcnow()
                        elif state == 'waiting':
                            oldServer.runningSince = None
                    oldServer.state = state

                oldServer.observers = server.get('observers', oldServer.observers)
                oldServer.hidden = server.get('hidden', oldServer.hidden)
                oldServer.type = server.get('type', oldServer.type)

    def _onGameReport(self, report):
        try:
            match = models.MatchModel(
                server = report['serverName'],
                type = report['type'],
                winningSide = report['winningSide'],
                time = report['time'])
            models.session.add(match)
            models.session.commit()

            for player in report['players']:
                playerId = self._getPlayer(player['name'], player['ai'], create=True).id
                models.session.add(MatchPlayerModel(
                    matchId = match.id,
                    playerId = playerId,
                    winner = player['side'] == report['winningSide'],
                    side = player['side']))
                models.session.commit()

        except KeyError as e:
            print(e)
            models.session.rollback()

    def _getPlayer(self, name, ai=False, online=False, create=False):
        player = next((p for p in self.onlinePlayers.values() if p.name == name and p.ai == ai), None)

        if player is None:
            if create:
                player = models.get_or_create(PlayerModel, name=name, ai=ai)
            else:
                player = models.session.query(PlayerModel).filter_by(name=name, ai=ai).one_or_none()
                if player is None: return None

            if online:
                player.lastActive = player.logonTime = datetime.utcnow()
                self.onlinePlayers[player.id] = player

        return player

    def _getPlayerId(self, name, ai=False):
        player = self._getPlayer(name, ai)
        if player is None: return None
        return player.id

    def _getServer(self, name, online=False):
        if name not in self.servers:
            if online:
                self.servers[name] = Server(name)
            else:
                return None
        return self.servers[name]
