import time
import json
import os
import traceback

import websocket
from pymitter import EventEmitter

email = None
token = None

# load account token
with open(os.path.dirname(os.path.realpath(__file__)) + '/token.json') as file:
    data = json.load(file)
    email = data['email']
    token = data['token']

def _cbHelper(method):
    return lambda *args: method(*args)

class IstroListener(EventEmitter):
    def __init__(self, login=False, root_address="ws://198.199.109.223:88"):
        super().__init__()
        self.root_address = root_address
        self.login = login
        self.stopped = True
        self.reconnecting = False

    def setLogin(self, login):
        self.login = login

    def connect(self):
        print("Starting IstroListener")

        self.ws = websocket.WebSocketApp(self.root_address,
                on_open=_cbHelper(self._onOpen),
                on_message=_cbHelper(self._onMessage),
                on_error=_cbHelper(self._onError),
                on_close=_cbHelper(self._onClose))

        # don't want exceptions to be caught
        self.ws._callback = lambda cb, *args: cb(self.ws, *args) if cb is not None else None

        self.stopped = False

        while not self.stopped:
            startTime = time.time()

            self.reconnecting = False
            self.ws.run_forever()

            if self.stopped: break
            if not self.reconnecting:
                time.sleep(max(5 - (time.time() - startTime), 1))
            print("Reconnecting IstroListener")

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
        print("IstroListener connected")
        ws.send('["registerBot"]')
        if self.login:
            ws.send(f'["authSignIn",{{"email":"{email}","token":"{token}"}}]')
            print("Logging in")

    def _onMessage(self, ws, msg):
        data = json.loads(msg);
        if len(data) == 1 and len(data[0]) == 1 and 'serverName' in data[0][0]:
            self.emit('gameReport', data[0][0])
        else:
            self.emit(data[0], *data[1:]);


    def _onError(self, ws, err):
        print("IstroListener Error:", end=" ")
        traceback.print_exception(type(err), err, err.__traceback__)
        self.emit('error', err)

    def _onClose(self, ws):
        print("IstroListener closed")
        self.emit('close', self.reconnecting)
