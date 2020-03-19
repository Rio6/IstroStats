#!/bin/env python

import signal
import threading
import time
import datetime
import code
import cherrypy

import istrolid
import models

istro = istrolid.Istrolid()

def timeFieldToEpoch(data):
    if data is None: return None
    for k,v in data.items():
        if isinstance(v, datetime.datetime):
            data[k] = v.timestamp()
    return data

@cherrypy.popargs('playerId')
class PlayerCtl:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, playerId=None):
        return timeFieldToEpoch(istro.getPlayerInfo(int(playerId)))

class RootCtl:
    def __init__(self):
        self.player = PlayerCtl()

    @cherrypy.expose()
    def index(self):
        return "hello"

def main():

    models.init()

    # istro listener in another thread
    istroThread = threading.Thread(target=istro.start)
    cherrypy.engine.subscribe('start', istroThread.start)
    cherrypy.engine.subscribe('exit', istro.stop)
    
    # web server
    cherrypy.quickstart(RootCtl(), '/', {
        'global': {
            'server.socket_port': 8000,
        }
    })

if __name__ == '__main__':
    main()
