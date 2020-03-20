#!/bin/env python

import os
import threading
import datetime
import json
import cherrypy

import istrolid
import models

DATABASE_URL='sqlite:///database.db?check_same_thread=False'

istro = istrolid.Istrolid()

# Date time to json
class DatetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
        return super().default(obj)
    def iterencode(self, value):
        for chunk in super().iterencode(value):
            yield chunk.encode("utf-8")

json_encoder = DatetimeJSONEncoder()
def json_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return json_encoder.iterencode(value)

@cherrypy.popargs('name')
class PlayerCtl:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        if 'name' in kwargs:
            return istro.getPlayerInfo(kwargs['name'])
        else:
            return istro.getPlayers(**kwargs)

@cherrypy.popargs('name')
class ServerCtl:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        if 'name' in kwargs:
            return(istro.getServerInfo(kwargs['name']))
        else:
            return istro.getServers(**kwargs)

@cherrypy.popargs('matchId')
class MatchCtl:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        if 'matchId' in kwargs:
            try:
                return(istro.getMatchInfo(int(kwargs['matchId'])))
            except ValueError:
                return None
        else:
            return istro.getMatches(**kwargs)

class APICtl:
    def __init__(self):
        self.player = PlayerCtl()
        self.server = ServerCtl()
        self.match = MatchCtl()

class RootCtl:
    def __init__(self):
        self.api = APICtl()

def main():

    models.init(DATABASE_URL)

    # istro listener in another thread
    istroThread = threading.Thread(target=istro.start)
    cherrypy.engine.subscribe('start', istroThread.start)
    cherrypy.engine.subscribe('exit', istro.stop)
    
    # web server
    cherrypy.quickstart(RootCtl(), '/', {
        'global': {
            'server.socket_port': 8000,
            'tools.json_out.handler': json_handler
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.dirname(os.path.realpath(__file__)) + '/frontend',
            'tools.staticdir.index': 'index.html'
        }
    })

if __name__ == '__main__':
    main()
