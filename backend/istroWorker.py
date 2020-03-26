import os
import json
import logging
from datetime import datetime

from . import models
from .models import PlayerModel, MatchModel, MatchPlayerModel, ServerModel, ServerPlayerModel
from .istroListener import IstroListener

ISTRO_NAME = "IstroStats"

class IstrolidWorker:
    def __init__(self):
        self.fullPlayers = False
        self.fullServers = False

        # load account token
        email = os.environ.get('EMAIL', None)
        token = os.environ.get('TOKEN', None)

        if email is None or token is None:
            with open('token.json') as file:
                data = json.load(file)
                if email is None:
                    email = data['email']
                if token is None:
                    token = data['token']


        self.listener = IstroListener(email, token, login=True)
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

        # remove non online servers and server-players
        models.session.query(ServerModel).filter(ServerModel.name.notin_(servers.keys())).delete(synchronize_session='fetch')
        models.session.commit()

        self._onServersDiff(servers)
        self._tryLoginless()

    def _tryLoginless(self):
        if self.fullPlayers and self.fullServers:
            logging.info("Reconnecting without login")
            self.listener.setLogin(False)
            self.listener.reconnect()

    def _onPlayersDiff(self, diff):
        for name, playerInfo in diff.items():
            if name == ISTRO_NAME: continue

            if playerInfo is None:
                # Player logged off
                playerInfo = self._getPlayer(name, create=True)
                playerInfo.lastActive = datetime.utcnow()
                playerInfo.logonTime = None
                playerInfo.mode = None

            else:
                player = self._getPlayer(name, updateOnline=True, create=True)

                if 'mode' in playerInfo:
                    player.mode = playerInfo['mode']
                    player.lastActive = datetime.utcnow()
                if 'color' in playerInfo:
                    player.color = str.format('#{:02x}{:02x}{:02x}{:02x}', *playerInfo['color'])

                player.rank = playerInfo.get('rank', player.rank)
                player.faction = playerInfo.get('faction', player.faction)

            models.session.commit()

    def _onServersDiff(self, diff):
        for name, serverInfo in diff.items():

            if serverInfo is None:
                # server offline
                models.session.query(ServerModel).filter_by(name=name).delete(synchronize_session='fetch')

            else:
                server = models.get_or_create(ServerModel, name=name)

                if 'players' in serverInfo:

                    def playerInfos():
                        playerInfos = serverInfo['players']
                        for info in playerInfos:
                            player = self._getPlayer(info['name'], info['ai'], updateOnline=False, create=True)
                            serverPlayer = models.get_or_create(ServerPlayerModel, serverId=server.id, playerId=player.id)
                            serverPlayer.side = info['side']
                            yield serverPlayer

                    server.players = [p for p in playerInfos()]

                if 'state' in serverInfo:
                    state = serverInfo['state']
                    # Record running time when state changes
                    if state != server.state:
                        if state == 'running':
                            server.runningSince = datetime.utcnow()
                        else:
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
                    winner = (player['side'] == report['winningSide']),
                    side = player['side']))

            models.session.commit()

        except KeyError as e:
            logging.error("Error adding new match: %s", e)
            models.session.rollback()

    # updateOnline: add player to online list
    # create: create player in db if it doesn't exist
    def _getPlayer(self, name, ai=False, updateOnline=False, create=False):
        if create:
            player = models.get_or_create(PlayerModel, name=name, ai=ai)
        else:
            player = models.session.query(PlayerModel).filter_by(name=name, ai=ai).one_or_none()
            if player is None: return None

        if updateOnline:
            now = datetime.utcnow()
            player.lastActive = now
            if player.logonTime is None:
                player.logonTime = now


        return player
