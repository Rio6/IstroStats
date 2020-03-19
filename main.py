#!/bin/env python

import signal
import threading
import time
import code

from wsgiref.simple_server import make_server
from tg import expose, TGController, MinimalApplicationConfigurator
from tg.configurator.components.sqlalchemy import SQLAlchemyConfigurationComponent
from tg.util import Bunch

import istrolid
import models
from models import PlayerModel, MatchModel, MatchPlayerModel

class RootController(TGController):
    def __init__(self, istro):
        self.istro = istro

    @expose()
    def index(self):
        return f"""
        {[(s.name, s.observers, s.state, str(s.runningSince), s.type, s.hidden, [(p.name, p.side, p.ai) for p in s.players]) for s in self.istro.servers.values()]}
        {[(p.name, p.mode, str(p.logonTime)) for p in self.istro.onlinePlayers.values()]}
         """

def main():
    # istro listener
    istro = istrolid.Istrolid()
    signal.signal(signal.SIGINT, lambda *args: istro.stop())

    # web server in other thread
    config = MinimalApplicationConfigurator()
    config.register(SQLAlchemyConfigurationComponent)
    config.update_blueprint({
        'root_controller': RootController(istro),
        'use_sqlalchemy': True,
        'sqlalchemy.url': 'sqlite:///database.db',
        'model': Bunch(
            DBSession=models.dbSession,
            init_model=models.init_model
        ),
    })

    app = config.make_wsgi_app()
    httpd = make_server('', 8000, app)
    serverThread = threading.Thread(target=httpd.serve_forever)
    serverThread.start()

    # istrolid listener in main thread
    istro.start()

    print("Stopping")
    httpd.shutdown()
    serverThread.join()
    httpd.server_close()

if __name__ == '__main__':
    main()
