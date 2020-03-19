from datetime import datetime

import models
from models import PlayerModel, MatchModel, MatchPlayerModel
from istro_listener import IstroListener

class OnlinePlayer:
    def __init__(self, name):
        self.name = name
        self.mode = None
        self.logonTime = datetime.utcnow()

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

    def start(self):
        self.listener.connect()

    def stop(self):
        self.listener.close()

    def _onPlayers(self, players):
        self.fullPlayers = True
        self._onPlayersDiff(players)
        self._tryLoginless()

    def _onServers(self, servers):
        self.fullServers = True
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
                self.onlinePlayers.pop(name, None)
            else:
                # in-memory data
                oldPlayer = self._getPlayer(name)
                oldPlayer.mode = player.get('mode', oldPlayer.mode)

                # database data
                dbPlayer = models.get_or_create(PlayerModel, name=name)
                dbPlayer.rank = player.get('rank', dbPlayer.rank)
                dbPlayer.lastActive = datetime.utcnow()
                models.dbSession.commit()

    def _onServersDiff(self, diff):
        for name, server in diff.items():
            if server is None:
                self.servers.pop(name, None)
            else:
                oldServer = self._getServer(name)
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
            models.dbSession.add(match)
            models.dbSession.commit()

            for player in report['players']:
                playerId = models.get_or_create(PlayerModel, name=player['name'], ai=player['ai']).id
                models.dbSession.add(MatchPlayerModel(
                    matchId = match.id,
                    playerId = playerId,
                    winner = player['side'] == report['winningSide'],
                    side = player['side']))
                models.dbSession.commit()

        except KeyError:
            models.dbSession.rollback()

    def _getPlayer(self, name):
        if name not in self.onlinePlayers:
            self.onlinePlayers[name] = OnlinePlayer(name)
        return self.onlinePlayers[name]

    def _getServer(self, name):
        if name not in self.servers:
            self.servers[name] = Server(name)
        return self.servers[name]
