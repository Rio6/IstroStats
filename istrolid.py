from datetime import datetime

import models
from models import PlayerModel, MatchModel, MatchPlayerModel
from istro_listener import IstroListener

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
                playerId = self._getPlayer(name, online=False).id
                self.onlinePlayers.pop(playerId, None)
            else:
                oldPlayer = self._getPlayer(name, online=True, create=True)

                # database data
                oldPlayer.rank = player.get('rank', oldPlayer.rank)
                oldPlayer.faction = player.get('faction', oldPlayer.faction)
                oldPlayer.lastActive = datetime.utcnow()
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
                serverName = report['serverName'],
                type = report['type'],
                winningSide = report['winningSide'],
                time = report['time'])
            models.session.add(match)
            models.session.commit()

            for player in report['players']:
                playerId = self._getPlayer(player['name'], player['ai'], online=False, create=True).id
                models.session.add(MatchPlayerModel(
                    matchId = match.id,
                    playerId = playerId,
                    winner = player['side'] == report['winningSide'],
                    side = player['side']))
                models.session.commit()

        except KeyError:
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
                player.logonTime = datetime.utcnow()
                self.onlinePlayers[player.id] = player

        return player

    def _getServer(self, name, online=False):
        if name not in self.servers:
            if online:
                self.servers[name] = Server(name)
            else:
                return None
        return self.servers[name]
