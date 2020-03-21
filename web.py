#!/bin/env python

import os
import datetime
import json
import cherrypy

from istroAPI import IstrolidAPI
import models

istro = IstrolidAPI()

# JSON encoder that can serialize datetime
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
    # web server
    cherrypy.quickstart(RootCtl(), '/', {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 8000)),
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
