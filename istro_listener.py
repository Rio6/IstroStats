import time
import websocket

def _class_cb(method):
    return lambda *args: method(*args)

class IstroListener:
    def __init__(self, root_address="ws://198.199.109.223:88"):
        self.root_address = root_address
        self.closed = False

    def run_forever(self):
        print("Starting IstroListener")
        self.ws = websocket.WebSocketApp(self.root_address,
                on_open=_class_cb(self.on_open),
                on_message=_class_cb(self.on_message),
                on_error=_class_cb(self.on_error),
                on_close=_class_cb(self.on_close))
        self.ws.run_forever()

    def close(self):
        self.closed = True
        self.ws.close()

    def on_open(self, ws):
        print("Connected")
        ws.send('["registerBot"]')

    def on_message(self, ws, msg):
        print(msg)

    def on_error(self, ws, err):
        print(err)

    def on_close(self, ws):
        if not self.closed:
            print("Reconnecting")
            time.sleep(1.0)
            self.connect()
        else:
            print("Closed")
