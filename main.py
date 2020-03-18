#!/bin/env python

import signal
import threading
import time
import code

from wsgiref.simple_server import make_server
from tg import expose, TGController, MinimalApplicationConfigurator
from tg.configurator.components.sqlalchemy import SQLAlchemyConfigurationComponent
from tg.util import Bunch

from istro_listener import IstroListener
from models import *

dbSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
dbMetadata = MetaData()
DeclarativeBase = declarative_base(metadata=dbMetadata)

class PlayerModel(DeclarativeBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(18), index=True, nullable=False)
    rank = Column(Integer)
    lastLogTime = Column(DateTime)

class MatchModel(DeclarativeBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    time = Column(Integer)
    serverType = Column(String(16))

class MatchPlayerModel(DeclarativeBase):
    __tablename__ = 'match_players'

    matchId = Column(Integer, nullable=False, primary_key=True)
    playerId = Column(Integer, nullable=False, primary_key=True)
    winner = Column(Boolean, nullable=False)
    side = Column(String(16))

class RootController(TGController):
    @expose()
    def index(self):
        return str(dbSession.query(MatchPlayerModel).one())

    @expose()
    def hello(self, **args):
        return 'Hello'

def init_model(engine):
    dbSession.configure(bind=engine)
    dbMetadata.create_all(engine)

def main():
    config = MinimalApplicationConfigurator()
    config.register(SQLAlchemyConfigurationComponent)
    config.update_blueprint({
        'root_controller': RootController(),
        'use_sqlalchemy': True,
        'sqlalchemy.url': 'sqlite:///database.db',
        'model': Bunch(
            DBSession=dbSession,
            init_model=init_model
        ),
    })

    # web server
    app = config.make_wsgi_app()
    httpd = make_server('', 8000, app)
    serverThread = threading.Thread(target=httpd.serve_forever)
    serverThread.start()

    # istro listener
    istro = IstroListener()
    signal.signal(signal.SIGINT, lambda *args: istro.close())
    istro.run_forever()

    print("Stopping")
    httpd.shutdown()
    serverThread.join()
    httpd.server_close()

if __name__ == '__main__':
    main()
