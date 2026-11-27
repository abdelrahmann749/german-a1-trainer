"""Run with: python -m unittest -v"""
import unittest
from datetime import date

import db
import srs
from main import is_correct
from words import UNITS


class TestSrs(unittest.TestCase):
    def test_right_answer_moves_up(self):
        self.assertEqual(srs.next_box(2, True), 3)

    def test_box_never_above_max(self):
        self.assertEqual(srs.next_box(5, True), 5)

    def test_wrong_answer_goes_to_box_1(self):
        self.assertEqual(srs.next_box(4, False), 1)

    def test_never_seen_is_due(self):
        self.assertTrue(srs.is_due(None, date(2026, 1, 1)))

    def test_future_date_not_due(self):
        self.assertFalse(srs.is_due("2026-01-05", date(2026, 1, 1)))


class TestDb(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")

    def test_wrong_then_right(self):
        today = date(2026, 1, 1)
        db.record_answer(self.conn, "Haus", False, today)
        db.record_answer(self.conn, "Haus", True, today)
        self.assertEqual(db.stats(self.conn), (1, 1, 1))
        self.assertEqual(db.get_due_text(self.conn, "Haus"), "2026-01-03")


class TestAnswers(unittest.TestCase):
    def test_article_optional(self):
        word = ("Tisch", "table", "طاولة", "der")
        self.assertTrue(is_correct("tisch", word))
        self.assertTrue(is_correct("Der Tisch", word))
        self.assertFalse(is_correct("die Tisch", word))


class TestData(unittest.TestCase):
    def test_words_valid_and_unique(self):
        words = [w for unit in UNITS.values() for w in unit]
        self.assertTrue(all(len(w) == 4 for w in words))
        self.assertTrue(all(w[3] in ("", "der", "die", "das") for w in words))
        german = [w[0] for w in words]
        self.assertEqual(len(german), len(set(german)))


if __name__ == "__main__":
    unittest.main()
