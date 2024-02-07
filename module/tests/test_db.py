import unittest
from db import DatabaseNya, GameRecordNya, UserScoreRecordNya, UserStatsRecordNya
from mjgame import MJGameNya

class TestDatabaseRecordsNya(unittest.TestCase):
    def test_game_record_equality(self):
        a = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        b = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertEqual(a, b)
        b1 = GameRecordNya("test:4321", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b1)
        b2 = GameRecordNya("test:1234", "unix:1704171600", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b2)
        b3 = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Texas", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertNotEqual(a, b3)
        b4 = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 6000, 51000])
        self.assertNotEqual(a, b4)

    def test_game_record_sorts_scores(self):
        record = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.assertEqual(record.users, ["Ichihime", "Amiya", "Frieren", "Neco Arc"])
        self.assertEqual(record.final_scores, [50000, 32000, 11000, 7000])
    
    def test_game_record_into_mjgame(self):
        record = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        mjgame = record.into_mjgame()
        self.assertEqual(mjgame.get_gameid(), "test:1234")
        self.assertEqual(mjgame.get_date(), 1704085200)
        self.assertEqual(mjgame.get_raw_scores(), {"Frieren": 11000, "Amiya": 32000, "Neco Arc": 7000, "Ichihime": 50000})
    
    def test_game_record_from_mjgame(self):
        mjgame = MJGameNya(1704085200, "test:1234", {"Frieren": 11000, "Amiya": 32000, "Neco Arc": 7000, "Ichihime": 50000})
        record = GameRecordNya.from_mjgame(mjgame)
        self.assertEqual(record, GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000]))

    def test_game_record_rejects_duplicate_users(self):
        self.assertRaises(ValueError, lambda: GameRecordNya("test:4321", "unix:1704085200", ["Neco Arc", "Neco Arc", "Neco Arc", "Neco Arc"], [25000, 25000, 25000, 25000]))

    def test_game_record_rejects_invalid_date(self):
        self.assertRaises(ValueError, lambda: GameRecordNya("test:4321", "invalid:date", ["Neco Arc", "Neco Arc", "Neco Arc", "Neco Arc"], [25000, 25000, 25000, 25000]))

    def test_user_score_record_equality(self):
        a = UserScoreRecordNya("Ichihime", "test:1234", "unix:1704085200", 1, 50000)
        b = UserScoreRecordNya("Ichihime", "test:1234", "unix:1704085200", 1, 50000)
        self.assertEqual(a, b)
        b1 = UserScoreRecordNya("Ichihime", "test:4321", "unix:1704085200", 1, 50000)
        self.assertNotEqual(a, b1)
        b2 = UserScoreRecordNya("Neco Arc", "test:1234", "unix:1704085200", 1, 50000)
        self.assertNotEqual(a, b2)
        b3 = UserScoreRecordNya("Ichihime", "test:1234", "unix:1704171600", 1, 50000)
        self.assertNotEqual(a, b3)
        b4 = UserScoreRecordNya("Ichihime", "test:1234", "unix:1704085200", 4, 50000)
        self.assertNotEqual(a, b4)
        b5 = UserScoreRecordNya("Ichihime", "test:1234", "unix:1704085200", 1, 25000)
        self.assertNotEqual(a, b5)
    
    def test_user_score_record_rejects_invalid_date(self):
        self.assertRaises(ValueError, lambda: UserScoreRecordNya("Ichihime", "test:1234", "invalid:date", 1, 50000))
    
    def test_user_stats_record_equality(self):
        a = UserStatsRecordNya("Ichihime", 89223, 30112, 205956)
        b = UserStatsRecordNya("Ichihime", 89223, 30112, 205956)
        self.assertEqual(a, b)
        b1 = UserStatsRecordNya("Neco Arc", 89223, 30112, 205956)
        self.assertNotEqual(a, b1)
        b2 = UserStatsRecordNya("Ichihime", 89224, 30112, 205956)
        self.assertNotEqual(a, b2)
        b3 = UserStatsRecordNya("Ichihime", 89223, 30113, 205956)
        self.assertNotEqual(a, b3)
        b4 = UserStatsRecordNya("Ichihime", 89223, 30112, 205957)
        self.assertNotEqual(a, b4)


class TestDatabase(unittest.TestCase):
    """
    Unit tests for database
    """
    def setUp(self):
        self.db = DatabaseNya(":memory:")
        self.g1 = GameRecordNya("test:1234", "unix:1704085200", ["Frieren", "Amiya", "Neco Arc", "Ichihime"], [11000, 32000, 7000, 50000])
        self.g2 = GameRecordNya("test:4321", "unix:1704171600", ["Frieren", "Texas", "Arcueid", "Ichihime"], [500, 80000, -10500, 30000])
        self.g3 = GameRecordNya("test:3333", "unix:1704258000", ["Amiya", "Texas", "Neco Arc", "Ichihime"], [90000, 0, -5000, 15000])
        self.g4 = GameRecordNya("test:9090", "unix:1704344400", ["Nijika", "Amiya", "Horn", "Ichihime",], [40000, -500, 5000, 55500])

    def test_new_game_doesnt_explode(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)

    def test_new_game_updates_stats(self):
        self.db.new_game(self.g1)
        self.db.new_game(self.g2)
        s1 = self.db.get_user_stats("Ichihime")
        self.assertEqual(s1, UserStatsRecordNya("Ichihime", 2, 1, 3))
        s2 = self.db.get_user_stats("Arcueid")
        self.assertEqual(s2, UserStatsRecordNya("Arcueid", 1, 0, 4))
    
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
            [UserScoreRecordNya("Ichihime", "test:1234", "unix:1704085200", 1, 50000),
            UserScoreRecordNya("Ichihime", "test:4321", "unix:1704171600", 2, 30000)]
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
        self.assertEqual(s1, UserStatsRecordNya("Ichihime", 1, 0, 2))
        s2 = self.db.get_user_stats("Arcueid")
        self.assertEqual(s2, UserStatsRecordNya("Arcueid", 1, 0, 4))
        s3 = self.db.get_user_stats("Amiya")
        self.assertEqual(s3, UserStatsRecordNya("Amiya", 0, 0, 0))
    
    def test_list_user_stats_sorting_games_played(self):
        [self.db.new_game(v) for v in [self.g1, self.g2, self.g3, self.g4]]
        expected = [
            UserStatsRecordNya("Ichihime", 4, 2, 6),
            UserStatsRecordNya("Amiya", 3, 1, 7),
            UserStatsRecordNya("Frieren", 2, 0, 6),
            UserStatsRecordNya("Neco Arc", 2, 0, 8),
            UserStatsRecordNya("Texas", 2, 1, 4),
            UserStatsRecordNya("Arcueid", 1, 0, 4),
            UserStatsRecordNya("Horn", 1, 0, 3),
            UserStatsRecordNya("Nijika", 1, 0, 2),
        ]
        ls = self.db.list_user_stats("games_played")
        self.assertEqual(ls, expected)
        ls = self.db.list_user_stats("games_played", 5)
        self.assertEqual(ls, expected[:5])
    
    def test_list_user_stats_sorting_games_won(self):
        [self.db.new_game(v) for v in [self.g1, self.g2, self.g3, self.g4]]
        expected = [
            UserStatsRecordNya("Ichihime", 4, 2, 6),
            UserStatsRecordNya("Amiya", 3, 1, 7),
            UserStatsRecordNya("Texas", 2, 1, 4),
            UserStatsRecordNya("Arcueid", 1, 0, 4),
            UserStatsRecordNya("Frieren", 2, 0, 6),
            UserStatsRecordNya("Horn", 1, 0, 3),
            UserStatsRecordNya("Neco Arc", 2, 0, 8),
            UserStatsRecordNya("Nijika", 1, 0, 2),
        ]
        ls = self.db.list_user_stats("games_won")
        self.assertEqual(ls, expected)
        ls = self.db.list_user_stats("games_won", 5)
        self.assertEqual(ls, expected[:5])
    
    def test_list_user_stats_sorting_avg_rank(self):
        [self.db.new_game(v) for v in [self.g1, self.g2, self.g3, self.g4]]
        expected = [
            UserStatsRecordNya("Ichihime", 4, 2, 6), # avg 1.50
            UserStatsRecordNya("Nijika", 1, 0, 2), # 2.00
            UserStatsRecordNya("Texas", 2, 1, 4), # avg 2.00
            UserStatsRecordNya("Amiya", 3, 1, 7), # avg 2.33
            UserStatsRecordNya("Frieren", 2, 0, 6), # avg 3.00
            UserStatsRecordNya("Horn", 1, 0, 3), # avg 3.00
            UserStatsRecordNya("Arcueid", 1, 0, 4), # avg 4.00
            UserStatsRecordNya("Neco Arc", 2, 0, 8), # avg 4.00
        ]
        ls = self.db.list_user_stats("avg_rank")
        self.assertEqual(ls, expected)
        ls = self.db.list_user_stats("avg_rank", 5)
        self.assertEqual(ls, expected[:5])
