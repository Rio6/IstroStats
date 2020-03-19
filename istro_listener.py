import time
import json
import os

import websocket
from pymitter import EventEmitter

email = None
token = None

# load account token
with open(os.path.dirname(os.path.realpath(__file__)) + '/token.json') as file:
    data = json.load(file)
    email = data['email']
    token = data['token']

def _class_cb(method):
    return lambda *args: method(*args)

class IstroListener(EventEmitter):
    def __init__(self, login=False, root_address="ws://198.199.109.223:88"):
        super().__init__()

        self.root_address = root_address
        self.login = login
        self.stopped = False;

        self.ws = websocket.WebSocketApp(self.root_address,
                on_open=_class_cb(self.on_open),
                on_message=_class_cb(self.on_message),
                on_error=_class_cb(self.on_error),
                on_close=_class_cb(self.on_close))

        # don't want exceptions to be caught
        self.ws._callback = lambda cb, *args: cb(self.ws, *args) if cb is not None else None

    def setLogin(self, login):
        self.login = login

    def connect(self):
        print("Starting IstroListener")
        while True:
            startTime = time.time()
            try:
                self.ws.run_forever()
                if self.stopped: break
            except Exception:
                time.sleep(max(10 - (time.time() - startTime), 1))
            print("Reconnecting IstroListener")

    def close(self):
        self.stopped = True
        self.ws.close()

    def reconnect(self):
        self.ws.close()

    def on_open(self, ws):
        print("IstroListener connected")
        ws.send('["registerBot"]')
        if self.login:
            ws.send(f'["authSignIn",{{"email":"{email}","token":"{token}"}}]')

    def on_message(self, ws, msg):
        data = json.loads(msg);
        if len(data) == 1 and len(data[0]) == 1 and 'serverName' in data[0][0]:
            self.emit('gameReport', data[0][0])
        else:
            self.emit(data[0], *data[1:]);


    def on_error(self, ws, err):
        print("IstroListener Error: " + str(err))
        self.emit('error', ws, err)

    def on_close(self, ws):
        print("IstroListener closed")
        self.emit('close', ws)
