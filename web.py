#!/bin/env python

import os
import datetime
import json
from decimal import Decimal

import cherrypy
import cherrypy_cors

from mako.exceptions import TemplateLookupException
from mako.lookup import TemplateLookup

from sqlalchemy import create_engine

from backend import IstrolidAPI, models

DATABASE_URL = 'sqlite:///database.db?check_same_thread=False'

root = os.path.abspath(os.path.dirname(__file__))
template = TemplateLookup(directories=os.path.join(root, 'templates'), module_directory=os.path.join(root, '__pycache__'))

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
    def __init__(self):
        self.istro = IstrolidAPI()

    @cherrypy.expose
    def player(self, **kwargs):
        return self.istro.getPlayers(**kwargs)

    @cherrypy.expose
    def server(self, **kwargs):
        return self.istro.getServers(**kwargs)

    @cherrypy.expose
    def match(self, **kwargs):
        return self.istro.getMatches(**kwargs)

    @cherrypy.expose
    def faction(self, **kwargs):
        return self.istro.getFactions(**kwargs)

    @cherrypy.expose
    def report(self, **kwargs):
        return self.istro.report(**kwargs)

    @cherrypy.expose
    def winrate(self, **kwargs):
        return self.istro.getPlayerWinRate(**kwargs)

    @cherrypy.expose
    def activefactions(self, **kwargs):
        return self.istro.getActiveFactions(**kwargs)

@cherrypy.popargs('page')
class RootCtl:
    def __init__(self):
        self.api = APICtl()

    @cherrypy.expose
    def index(self, page='index', **_):
        try:
            return template.get_template('base.mako').render(page=page, root=root)
        except TemplateLookupException:
            raise cherrypy.NotFound(page)

def main():
    engine = create_engine(os.environ.get('DATABASE_URL', DATABASE_URL))
    models.init_models(engine)

    # web server
    cherrypy_cors.install()
    cherrypy.config.update({
        'global': {
            'environment': os.environ.get('ENVIRONMENT'),
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 8000)),
            'log.screen': True,
            'tools.proxy.on': True,
            'tools.proxy.base': os.environ.get('HOST'),
            'tools.json_out.handler': json_handler,
        }
    })
    cherrypy.tree.mount(RootCtl(), '/', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(root, 'static'),
            'cors.expose_public.on': True,
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    main()
