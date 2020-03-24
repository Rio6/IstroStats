import os
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()
session = None

class PlayerModel(DeclarativeBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    rank = Column(Integer, default=0)
    faction = Column(String, default='')
    color = Column(String, default='#000000ff')
    ai = Column(Boolean, default=False)
    lastActive = Column(DateTime)
    mode = Column(String)
    logonTime = Column(DateTime)

class ServerPlayerModel(DeclarativeBase):
    __tablename__ = 'server_players'
    id = Column(Integer, primary_key=True)
    serverId = Column(Integer, ForeignKey('servers.id'), nullable=False)
    playerId = Column(Integer, ForeignKey('players.id'), nullable=False)
    side = Column(String)

class MatchPlayerModel(DeclarativeBase):
    __tablename__ = 'match_players'

    id = Column(Integer, primary_key=True)
    matchId = Column(Integer, ForeignKey('matches.id'), index=True, nullable=False)
    playerId = Column(Integer, ForeignKey('players.id'), index=True, nullable=False)
    winner = Column(Boolean)
    side = Column(String)

class ServerModel(DeclarativeBase):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    observers = Column(Integer, default=0)
    type = Column(String)
    state = Column(String)
    hidden = Column(Boolean)
    runningSince = Column(DateTime)

    players = relationship(ServerPlayerModel, cascade='all, delete-orphan')

class MatchModel(DeclarativeBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    server = Column(String, nullable=False)
    finished = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    type = Column(String)
    winningSide = Column(String)
    time = Column(Float)

    players = relationship(MatchPlayerModel)

# https://stackoverflow.com/a/6078058/6023997
def get_or_create(model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance

def init_models(engine):
    global session
    DeclarativeBase.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
