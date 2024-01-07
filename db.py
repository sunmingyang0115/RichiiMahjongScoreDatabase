def _init():
  import sqlite3
  from typing import List, Tuple

  global GameRecord
  class GameRecord:
    game_id: str
    date: str
    users: List[str]
    final_scores: List[int]

    def __init__(self, game_id: str, date: str, users: List[str], final_scores: List[int]):
      zipped = list(zip(users, final_scores))
      zipped.sort(key=lambda x: x[1])
      users, final_scores = zip(*zipped)
      self.game_id = game_id
      self.date = date
      self.users = users
      self.final_scores = final_scores

  global UserScoreRecord
  class UserScoreRecord:
    user_id: str
    game_id: str
    date: str
    rank: int
    final_score: int

    def __init__(self, user_id: str, game_id: str, date: str, rank: int, final_score: int):
      self.user_id = user_id
      self.game_id = game_id
      self.date = date
      self.rank = rank
      self.final_score = final_score

  global Database
  class Database:
    """
    Holds a simple database used to store user data
    """
    
    def __init__(self, path = "db.sqlite"):
      """
      Initializes the database to read from a file argument. Defaults to db.sqlite
      """
      self.conn = sqlite3.connect(path)
      self.conn.execute("""
create table "user_scores" (
	"game_id"	integer not null,
	"user_id"	text not null,
	"date"	text not null,
	"rank"	integer not null,
	"score"	integer not null
)
""")
      self.conn.isolation_level = None
    
    def new_game(self, record: GameRecord):
      c = self.conn.cursor()
      c.execute("begin")
      for i in range(len(record.users)):
        c.execute(
          "insert into user_scores (game_id, user_id, date, rank, score) values (?1, ?2, ?3, ?4, ?5)",
          (record.game_id, record.users[i], record.date, i + 1, record.final_scores[i])
        )
      c.execute("commit")
      c.close()

    def get_user_games(self, user_id: str) -> List[UserScoreRecord]:
      c = self.conn.cursor()
      c.execute("select game_id, rank, score from user_scores where user_id = ?1", (user_id,))
      scores = [UserScoreRecord(user_id, v[0], v[1], v[2]) for v in c.fetchall()]
      c.close()
      return scores

    def get_game(self, game_id: str) -> List[UserScoreRecord]:
      c = self.conn.cursor()
      c.execute("select user_id, date, score from user_scores where game_id = ?1", (game_id,))
      users, dates, scores = zip(*c.fetchall())
      game = GameRecord(game_id, dates[0], users, scores)
      c.close()
      return game
    
    def delete_game(self, game_id: str):
      c = self.conn.cursor()
      c.execute("begin")
      c.execute("delete from user_scores where game_id = ?1", (game_id,))
      c.execute("commit")
      c.close()

_init()