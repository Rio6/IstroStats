#!/bin/env python

import signal
import threading
import time
import code
import cherrypy

import istrolid
import models
from models import PlayerModel, MatchModel, MatchPlayerModel

@cherrypy.popargs('hi')
class TestController:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, hi):
        return {'abc': hi}

class RootController:
    def __init__(self, istro):
        self.istro = istro
        self.test = TestController()

    @cherrypy.expose()
    def index(self):
        return f"""
        {[(s.name, s.observers, s.state, str(s.runningSince), s.type, s.hidden, [(p.name, p.side, p.ai) for p in s.players]) for s in self.istro.servers.values()]}
        {[(p.name, p.mode, str(p.logonTime)) for p in self.istro.onlinePlayers.values()]}
         """

def main():
    # istro listener in another thread
    istro = istrolid.Istrolid()
    istroThread = threading.Thread(target=istro.start)
    cherrypy.engine.subscribe('start', istroThread.start)
    cherrypy.engine.subscribe('exit', istro.stop)
    
    # web server
    cherrypy.quickstart(RootController(istro), '/', {
        'global': {
            'server.socket_port': 8000,
        }
    })

if __name__ == '__main__':
    main()
