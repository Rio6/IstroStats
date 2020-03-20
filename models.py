from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL='sqlite:///database.db?check_same_thread=False'

DeclarativeBase = declarative_base()

engine = None
session = None

class PlayerModel(DeclarativeBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(18), index=True, nullable=False)
    rank = Column(Integer, default=0)
    faction = Column(String(8), default='')
    ai = Column(Boolean, default=False)
    lastActive = Column(DateTime)

    # in-memory fields
    mode = None
    logonTime = None

class MatchModel(DeclarativeBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    server = Column(String(32), nullable=False)
    finished = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    type = Column(String(16))
    winningSide = Column(String(16))
    time = Column(Float)

class MatchPlayerModel(DeclarativeBase):
    __tablename__ = 'match_players'

    id = Column(Integer, primary_key=True)
    matchId = Column(Integer, nullable=False, index=True)
    playerId = Column(Integer, nullable=False, index=True)
    winner = Column(Boolean, nullable=False)
    side = Column(String(16))

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

def init():
    global engine, session
    engine = create_engine(DATABASE_URL)
    session = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
    DeclarativeBase.metadata.create_all(engine)
