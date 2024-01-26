import unittest
from db import Database, GameRecord, UserScoreRecord, UserStatsRecord

class TestDatabaseRecords(unittest.TestCase):
    def test_game_record_equality(self):
        a = GameRecord("test:1234", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        b = GameRecord("test:1234", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertEqual(a, b)
        b1 = GameRecord("test:4321", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b1)
        b2 = GameRecord("test:1234", "2024-02-14", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b2)
        b3 = GameRecord("test:1234", "2024-01-01", ["Frieren", "Texas", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b3)
        b4 = GameRecord("test:1234", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 6000, 51000])
        self.assertNotEqual(a, b4)

    def test_game_record_sorts_scores(self):
        record = GameRecord("test:1234", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertEqual(record.users, ["Ichihime", "Amiya", "Frieren", "Neco Arc"])
        self.assertEqual(record.final_scores, [50000, 32000, 11000, 7000])
    
    def test_game_record_rejects_duplicate_users(self):
        self.assertRaises(ValueError, lambda: GameRecord("test:4321", "2024-01-01", ["Neco Arc", "Neco Arc", "Neco Arc", "Neco Arc"], [25000, 25000, 25000, 25000]))

    def test_user_score_record_equality(self):
        a = UserScoreRecord("Ichihime", "test:1234", "2024-01-01", 1, 50000)
        b = UserScoreRecord("Ichihime", "test:1234", "2024-01-01", 1, 50000)
        self.assertEqual(a, b)
        b1 = UserScoreRecord("Ichihime", "test:4321", "2024-01-01", 1, 50000)
        self.assertNotEqual(a, b1)
        b2 = UserScoreRecord("Neco Arc", "test:1234", "2024-01-01", 1, 50000)
        self.assertNotEqual(a, b2)
        b3 = UserScoreRecord("Ichihime", "test:1234", "2024-02-14", 1, 50000)
        self.assertNotEqual(a, b3)
        b4 = UserScoreRecord("Ichihime", "test:1234", "2024-01-01", 4, 50000)
        self.assertNotEqual(a, b4)
        b5 = UserScoreRecord("Ichihime", "test:1234", "2024-01-01", 1, 25000)
        self.assertNotEqual(a, b5)
    
    def test_user_stats_record_equality(self):
        a = UserStatsRecord("Ichihime", 89223, 30112, 205956)
        b = UserStatsRecord("Ichihime", 89223, 30112, 205956)
        self.assertEqual(a, b)
        b1 = UserStatsRecord("Neco Arc", 89223, 30112, 205956)
        self.assertNotEqual(a, b1)
        b2 = UserStatsRecord("Ichihime", 89224, 30112, 205956)
        self.assertNotEqual(a, b2)
        b3 = UserStatsRecord("Ichihime", 89223, 30113, 205956)
        self.assertNotEqual(a, b3)
        b4 = UserStatsRecord("Ichihime", 89223, 30112, 205957)
        self.assertNotEqual(a, b4)


class TestDatabase(unittest.TestCase):
    """
    Unit tests for database
    """
    def setUp(self):
        self.db = Database(":memory:")
        self.g1 = GameRecord("test:1234", "2024-01-01", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.g2 = GameRecord("test:4321", "2024-01-02", ["Frieren", "Texas", "Arcueid", "Ichihime"], [500, 80000, -10500, 30000])

    def test_new_game_doesnt_explode(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)

    def test_new_game_updates_stats(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)
        s1 = self.db.get_user_stats("Ichihime")
        self.assertEqual(s1, UserStatsRecord("Ichihime", 2, 1, 3))
        s2 = self.db.get_user_stats("Arcueid")
        self.assertEqual(s2, UserStatsRecord("Arcueid", 1, 0, 4))
    
    def test_new_game_rejects_duplicate_id(self):
        self.db.new_game(self.g1)
        self.assertRaises(ValueError, lambda: self.db.new_game(self.g1))

    def test_get_game(self):
        self.db.new_game(self.g1)
        retrieved = self.db.get_game("test:1234")
        self.assertEqual(self.g1, retrieved)
    
    def test_get_game_returns_none(self):
        self.assertEqual(self.db.get_game("not exist"), None)

    def test_get_user_games(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)
        games = self.db.get_user_games("Ichihime")
        games.sort()
        self.assertEqual(games,
            [UserScoreRecord("Ichihime", "test:1234", "2024-01-01", 1, 50000),
            UserScoreRecord("Ichihime", "test:4321", "2024-01-02", 2, 30000)]
        )

    def test_get_user_games_returns_empty(self):
        self.assertEqual(self.db.get_user_games("not exist"), [])

    def test_delete_game(self):
        self.db.new_game(self.g1)
        self.db.delete_game("test:1234")
        self.assertEqual(self.db.get_game("test:1234"), None)
    
    def test_delete_game_updates_stats(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)
        self.db.delete_game("test:1234")
        s1 = self.db.get_user_stats("Ichihime")
        self.assertEqual(s1, UserStatsRecord("Ichihime", 1, 0, 2))
        s2 = self.db.get_user_stats("Arcueid")
        self.assertEqual(s2, UserStatsRecord("Arcueid", 1, 0, 4))
        s3 = self.db.get_user_stats("Amiya")
        self.assertEqual(s3, UserStatsRecord("Amiya", 0, 0, 0))