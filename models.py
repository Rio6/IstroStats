from sqlalchemy import MetaData, Column, Integer, DateTime, String, Boolean
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

def init_model(engine):
    dbSession.configure(bind=engine)
    dbMetadata.create_all(engine)
