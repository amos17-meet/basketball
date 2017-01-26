from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from database_setup import *


engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


amos=Coach(name="amos",
			email="amos.ro7@gmail.com",
			password="123",
			nickname="amosrottenberg")

team1=Starting_5 (name="1")

ido=Player(name="ido",
	player_position=1,
	three_points=40,
	two_points=50,
	one_on_one=7,
	defense=8,
	)

session.add(team1)
session.add(amos)
session.add(ido)

amos.players.append(ido)

amos.starting_5s.append(team1)

ido.player_starting_5s.append(team1)

#ido.player_teams.append(team1)






session.commit()
			

