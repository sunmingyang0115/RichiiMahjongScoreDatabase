def _init():
  import sqlite3

  global Database
  class Database:
    """
    Holds a simple database used to store user data
    """
    
    def __init__(self):
      """
      Initializes the database to read from a file called "db.sqlite"
      """
      self.conn = sqlite3.connect("db.sqlite")
      self.conn.execute("create table if not exists \"user_money\" (\"user\" text not null unique, \"money\" integer not null, primary key(\"user\"))")
      self.conn.isolation_level = None
    
    def get(self, user: str) -> int | None:
      """
      Retrieves the money for a single user
      """
      c = self.conn.cursor()
      c.execute("select money from user_money where user = ?1", (user,))
      money = c.fetchone()
      c.close()
      if money is None:
        return money
      else:
        return money[0]
  
    def add(self, user: str, add: int) -> int:
      """
      Adds money to a user
      """
      c = self.conn.cursor()
      c.execute("begin")
      c.execute("select money from user_money where user = ?1", (user,))
      (money,) = c.fetchone()
      money += add
      c.execute("update user_money set money = ?2 where user = ?1 ", (user, money))
      c.execute("commit")
      c.close()
      return money
    
    def set(self, user: str, money: int):
      """
      Sets user's money to a certain amount
      """
      c = self.conn.cursor()
      c.execute("insert into user_money (user, money) values (?1, ?2) on conflict do update set money = ?2 where user = ?1", (user, money))
      c.close()
      

_init()