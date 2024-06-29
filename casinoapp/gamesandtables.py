class Game:
  games = []
  subset_games = {}
  def __init__(self, name, description, maxplayers, rules="Insert rules here", subsetof=None):
    self.id = len(Game.games) + 1
    self.name = name
    self.description = description
    self.max_players = maxplayers
    self.tables = []
    self.bet_amounts = []
    self.subset_of = subsetof
    self.rules = rules

    if subsetof not in Game.subset_games.keys():
      Game.subset_games[subsetof] = []
      
    Game.subset_games[subsetof].append(self)
    Game.games.append(self)

  def instantiate_tables(self, minbetval=5, betranges=4, no_tables=10):
    for i in range(betranges):
      self.bet_amounts.append((minbetval, minbetval * 20))
      for _ in range(no_tables): # 10 tables per bet range
        self.tables.append(Table(
          game = self.name,
          max_bet = minbetval * 20,
          min_bet = minbetval,
          max_players = self.max_players
        ))

      minbetval *= 5 if i % 2 == 0 else 4
      
  @classmethod
  def instantiate_all_tables(cls):
    for game in cls.games:
      game.instantiate_tables()

  @classmethod
  def print_all_tables(cls):
    for game in cls.games:
      for table in game.tables:
        print(table)
      print()

  @classmethod
  def print_all_subset_games(cls):
    for key in cls.subset_games.keys():
      print(f"{key}: {cls.subset_games[key]}")

  @classmethod
  def find_game(cls, gamename: str):
    for game in cls.games:
      if game.name == gamename:
        return game
    return None
    
  def __repr__(self):
    return f"Game({self.name}, Tables: {len(self.tables)})"


class Table:
  def __init__(self, game, max_bet, min_bet=1, max_players = 3):
    self.game = game
    self.max_bet = max_bet
    self.min_bet = min_bet
    self.max_players = max_players

  def __repr__(self):
    return f"Table({self.game}, Min: ${self.min_bet}, Max: ${self.max_bet}, MaxPlayers: {self.max_players})"


# *********************************
# **** INSTANTIATING EACH GAME ****
# *********************************

blackjack = Game(name="Blackjack", description="Chase 21, make split-second decisions, and outplay the dealer in this heart-pounding game of cards and cunning!", maxplayers=3)

texasholdem_poker = Game(name="Texas Hold'em", description="Navigate the high-stakes world of community cards and cunning bluffs in the ultimate poker showdown for glory at the green felt!", maxplayers=5, subsetof="Poker") 

omaha_poker = Game(name="Omaha", description="Four hole cards, a flood of possibilities – outsmart opponents and seize victory in this dynamic poker variant!", maxplayers=5, subsetof="Poker") 

sevenstud_poker = Game(name="Seven Card Stud", description="Classic and strategic, navigate the twists of this stud poker game to assemble the best possible hand and conquer the table.", maxplayers=5, subsetof="Poker") 

roulette = Game(name="Roulette", description="A whirlwind of anticipation, the spinning wheel, the click of fate. In the casino's pulse, fortunes turn with every spin.", maxplayers=7)




# ************************
# **** FUNCTION CALLS ****
# ************************

Game.instantiate_all_tables()


# Game.print_all_subset_games()
  