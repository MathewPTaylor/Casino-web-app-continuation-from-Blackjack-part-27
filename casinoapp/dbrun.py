from casinoapp import app, db
from casinoapp.models import *
from casinoapp.gamesandtables import Game, Table


def create_all():
  with app.app_context():
    db.create_all()

def drop_all():
  with app.app_context():
    db.drop_all()


def create_table(table):
  with app.app_context():
    table.__table__.create(db.engine)

def drop_table(table):
  with app.app_context():
    table.__table__.drop(db.engine)

def initialise_games():
  '''Initialise every game that is instantiated
     in the gamesandtables.py file.'''
  
  with app.app_context():
    for game in Game.games:
      print(game)
      gamedb = Games.query.filter_by(name=game.name).first()
      
      if gamedb is None:
        db.session.add(Games(
          name = game.name,
          description = game.description,
          subset_of = game.subset_of,
          rules = game.rules
        ))
        db.session.commit()
        print("SUCCESSFULLY INITIALISED", game)
      else:
        print("GAME INITIALISED ALREADY", gamedb)

def initialise_game_tables(game=None):
  with app.app_context():
    if game is None: # instantiate tables for every game
      gamesdb = Games.query.all()
      if len(gamesdb) == 0:
        print("NO GAMES INITIALISED")
        return
      
      for i in range(len(Game.games)):
        for table in Game.games[i].tables:
          db.session.add(Tables(game_id=gamesdb[i].id,
                                max_bet=table.max_bet,
                                min_bet=table.min_bet,
                                max_players=table.max_players))
          db.session.commit()
        print("SUCCESSFULLY INITIALISED TABLES FOR:", gamesdb[i])
    else:
      gamedb = Games.query.filter_by(name=game.name).first()
      for table in game.tables:
        db.session.add(Tables(game_id=gamedb.id,
                              max_bet=table.max_bet,
                              min_bet=table.min_bet,
                              max_players=table.max_players))
        db.session.commit()
        
      print("SUCCESSFULLY INITIALISED TABLES FOR:", gamedb)
      


def print_db_instances(table):
  with app.app_context():
    instances = table.query.all()
    for instance in instances:
      print(instance)

  if len(instances) == 0:
    print("Empty Table")
    
  print("Number of records:", len(instances))
  

