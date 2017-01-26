from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func

Base = declarative_base()

class Coach(Base):
    __tablename__ = 'coach'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    nickname = Column(String)
    #players= relationship("Player")
    starting_5s=relationship("Starting_5", back_populates="coach")
    players=relationship("Player", back_populates="coach")




association_table = Table('association', Base.metadata,
    Column('player_id', Integer, ForeignKey('player.id')),
    Column('starting_5_name', Integer, ForeignKey('starting_5.name')))

    


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    #coach_id=Column(Integer, ForeignKey('coach.id'))
    coach_id = Column(Integer, ForeignKey("coach.id"))
    coach = relationship("Coach", back_populates="players")
    player_starting_5s=relationship("Starting_5", secondary=association_table, back_populates="players")
    player_position= Column(String)
    three_points = Column(String)
    two_points = Column(String)
    one_on_one = Column(String)
    defense = Column(String)


class Starting_5(Base):
    __tablename__ = 'starting_5'
    id = Column (Integer, primary_key=True)
    coach_id = Column(Integer, ForeignKey("coach.id"))
    coach = relationship("Coach", back_populates="starting_5s")
    name = Column(String)
    players =relationship("Player", secondary=association_table, back_populates="player_starting_5s")


