from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

engine = None
session = None

class PlayerModel(DeclarativeBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(18), index=True, nullable=False)
    rank = Column(Integer, default=0)
    faction = Column(String(8), default='')
    color = Column(String(9), default='#000000ff')
    ai = Column(Boolean, default=False)
    lastActive = Column(DateTime)
    mode = Column(String(18))
    logonTime = Column(DateTime)

class ServerPlayerModel(DeclarativeBase):
    __tablename__ = 'server_players'
    id = Column(Integer, primary_key=True)
    serverId = Column(Integer, ForeignKey('servers.id'))
    playerId = Column(Integer, ForeignKey('players.id'))
    side = Column(String(18))

    UniqueConstraint(serverId, playerId)

class MatchPlayerModel(DeclarativeBase):
    __tablename__ = 'match_players'

    id = Column(Integer, primary_key=True)
    matchId = Column(Integer, ForeignKey('matches.id'), index=True)
    playerId = Column(Integer, ForeignKey('players.id'), index=True)
    winner = Column(Boolean, nullable=False)
    side = Column(String(16))

    UniqueConstraint(matchId, playerId)

class ServerModel(DeclarativeBase):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    observers = Column(Integer, default=0)
    type = Column(String(16))
    state = Column(String(16))
    hidden = Column(Boolean)
    runningSince = Column(DateTime)

    players = relationship(ServerPlayerModel)

class MatchModel(DeclarativeBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    server = Column(String(32), nullable=False)
    finished = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    type = Column(String(16))
    winningSide = Column(String(18))
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

def init(dbUrl):
    global engine, session
    engine = create_engine(dbUrl)
    session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
    DeclarativeBase.metadata.create_all(engine)
