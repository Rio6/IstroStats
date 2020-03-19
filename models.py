from sqlalchemy import MetaData, Column, Integer, DateTime, String, Boolean, Float
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base

dbSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
dbMetadata = MetaData()
DeclarativeBase = declarative_base(metadata=dbMetadata)

class PlayerModel(DeclarativeBase):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String(18), index=True, nullable=False)
    rank = Column(Integer, default=0)
    ai = Column(Boolean, default=False)
    lastActive = Column(DateTime)

class MatchModel(DeclarativeBase):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    serverName = Column(String(32), nullable=False)
    type = Column(String(16), nullable=False)
    winningSide = Column(String(16))
    time = Column(Float)

class MatchPlayerModel(DeclarativeBase):
    __tablename__ = 'match_players'

    matchId = Column(Integer, nullable=False, primary_key=True)
    playerId = Column(Integer, nullable=False, primary_key=True)
    winner = Column(Boolean, nullable=False)
    side = Column(String(16))

def init_model(engine):
    dbSession.configure(bind=engine)
    dbMetadata.create_all(engine)

# https://stackoverflow.com/a/6078058/6023997
def get_or_create(model, **kwargs):
    instance = dbSession.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        dbSession.add(instance)
        return instance
