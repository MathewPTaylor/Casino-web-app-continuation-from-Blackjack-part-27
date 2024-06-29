from casinoapp import db, login_manager
from flask_login import UserMixin
from casinoapp.enums import TransactionType, GameOutcome
import datetime

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  # all of these fields are string because theyre going to get hashed when it is stored in the database
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  balance = db.Column(db.Integer, nullable=False, default=0)
  image_file = db.Column(db.String(20),
                         nullable=False,
                         default='default_pfp.jpg')
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
  banned = db.Column(db.Boolean, nullable=False, default=False)
  slot_spins = db.Column(db.Integer, nullable=False, default=0)
  
  game_records = db.relationship('GameRecords', backref='user', lazy=True)
  transactions = db.relationship('Transactions', backref='user', lazy=True)

  def __repr__(self):
    return f"User({self.username}, {self.email}, ${self.balance})"


class Games(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False, unique=True)
  description = db.Column(db.String, nullable=False)
  subset_of = db.Column(db.String, nullable=True)
  rules = db.Column(db.String, nullable=False)
  
  tables = db.relationship('Tables', backref='game', lazy=True)

  def __repr__(self):
    return f"DBGame({self.id}, {self.name}, Tables: {len(self.tables)})"


class Tables(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.ForeignKey('games.id'), nullable=False)
  max_bet = db.Column(db.Integer, nullable=False)
  min_bet = db.Column(db.Integer, nullable=False)
  max_players = db.Column(db.Integer, nullable=False, default=3) # -1 max_players mean infinite players per table, basically each instance of a table will be created at runtime
  current_players = db.Column(db.String, default="[]") # gonna be stored as a JSON string, gonna store the player's id
  no_players = db.Column(db.Integer, nullable=False, default=0)
  
  game_records = db.relationship('GameRecords', backref='table', lazy=True)

  def __repr__(self):
    return f"DBTable({self.id}, GameID: {self.game_id}, ${self.min_bet}-${self.max_bet}, Players: {self.current_players})"


class Transactions(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  amount = db.Column(db.Double, nullable=False)
  transaction_type = db.Column(db.Enum(TransactionType), nullable=False)


class GameRecords(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)
  bet_amount = db.Column(db.Double, nullable=False)
  outcome = db.Column(db.Enum(GameOutcome), nullable=False)
