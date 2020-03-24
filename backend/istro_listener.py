import time
import json
import os
import logging

import websocket
from pymitter import EventEmitter

email = None
token = None

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

class IstroListener(EventEmitter):
    def __init__(self, login=False, root_address="ws://198.199.109.223:88"):
        super().__init__()
        self.root_address = root_address
        self.login = login
        self.stopped = True
        self.reconnecting = False

    # whether to use email+token to obtain full game information
    def setLogin(self, login):
        self.login = login

    def connect(self):
        logging.info("Starting IstroListener")

        self.ws = websocket.WebSocketApp(self.root_address,
                on_open=self._onOpen,
                on_message=self._onMessage,
                on_error=self._onError,
                on_close=self._onClose)

        def ws_callback(cb, *args):
            if cb is None: return
            try:
                cb(self.ws, *args)
            except Exception as e:
                logging.error("IstroListener callback error: %s", e)

        self.ws._callback = ws_callback

        self.stopped = False

        while not self.stopped:
            startTime = time.time()

            self.reconnecting = False
            self.ws.run_forever()

            if self.stopped: break
            if not self.reconnecting: # add timeout between auto reconnects
                time.sleep(max(5 - (time.time() - startTime), 1))
            logging.info("Reconnecting IstroListener")

    def close(self):
        if self.stopped: return
        self.stopped = True
        self.ws.close()

    def reconnect(self):
        if self.stopped:
            self.connect()
        else:
            self.reconnecting = True
            self.ws.close()

    def _onOpen(self, ws):
        logging.info("IstroListener connected")
        ws.send('["registerBot"]')
        if self.login:
            ws.send(f'["authSignIn",{{"email":"{email}","token":"{token}"}}]')

    def _onMessage(self, ws, msg):
        data = json.loads(msg);

        if data[0] == 'authError':
            logging.error("Login error: %s", data[1])
        elif data[0] == 'login':
            logging.info("Logged in")

        if len(data) == 1 and len(data[0]) == 1 and 'serverName' in data[0][0]:
            self.emit('gameReport', data[0][0])
        else:
            self.emit(data[0], *data[1:]);


    def _onError(self, ws, err):
        logging.error("IstroListener Error: %s", err)
        self.emit('error', err)

    def _onClose(self, ws):
        logging.info("IstroListener closed")
        self.emit('close', self.reconnecting)
