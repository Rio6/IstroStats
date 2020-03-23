#!/bin/env python

import os
import datetime
import json
from decimal import Decimal
import cherrypy

from istroAPI import IstrolidAPI

istro = IstrolidAPI()

# JSON encoder that can serialize datetime
class DatetimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
        elif isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)
    def iterencode(self, value):
        for chunk in super().iterencode(value):
            yield chunk.encode("utf-8")

json_encoder = DatetimeJSONEncoder()
def json_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return json_encoder.iterencode(value)

@cherrypy.tools.json_out()
class APICtl:
    @cherrypy.expose
    def player(self, **kwargs):
        return istro.getPlayers(**kwargs)

    @cherrypy.expose
    def server(self, **kwargs):
        return istro.getServers(**kwargs)

    @cherrypy.expose
    def match(self, **kwargs):
        return istro.getMatches(**kwargs)

    @cherrypy.expose
    def faction(self, **kwargs):
        return istro.getFactions(**kwargs)

    @cherrypy.expose
    def report(self, **kwargs):
        return istro.report(**kwargs)

class RootCtl:
    def __init__(self):
        self.api = APICtl()

def main():
    # web server
    cherrypy.config.update({
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 8000)),
            'tools.json_out.handler': json_handler
        }
    })
    cherrypy.tree.mount(RootCtl(), '/', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.dirname(os.path.realpath(__file__)) + '/frontend',
            'tools.staticdir.index': 'index.html'
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
