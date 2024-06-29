import enum

class TransactionType(enum.Enum):
  withdrawal = "WITHDRAWAL"
  deposit = "DEPOSIT"

class GameOutcome(enum.Enum):
  win = "WIN"
  lose = "LOSE"
  draw = "PUSH"

class BetAmount(enum.Enum):
  low_stakes = {
    "min_bet": 5,
    "max_bet": 100
  }
  medium_low_stakes = {
    "min_bet": 25,
    "max_bet": 500
  }
  medium_high_stakes = {
    "min_bet": 100,
    "max_bet": 2000
  }
  high_stakes = {
    "min_bet": 500,
    "max_bet": 10000
  }
  