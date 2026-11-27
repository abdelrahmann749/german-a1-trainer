"""Saving progress in a SQLite file (one table, one row per word)."""
import sqlite3
from datetime import date

import srs


def connect(path="progress.db"):
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS progress (
               german TEXT PRIMARY KEY,
               box INTEGER NOT NULL,
               due TEXT NOT NULL,
               right_count INTEGER NOT NULL DEFAULT 0,
               wrong_count INTEGER NOT NULL DEFAULT 0
           )"""
    )
    return conn


def get_due_text(conn, german):
    """Return the due date text of a word, or None if never practiced."""
    row = conn.execute("SELECT due FROM progress WHERE german = ?", (german,)).fetchone()
    return row[0] if row else None


def record_answer(conn, german, correct, today=None):
    """Update the word's box and due date after an answer."""
    today = today or date.today()
    row = conn.execute("SELECT box FROM progress WHERE german = ?", (german,)).fetchone()
    old_box = row[0] if row else 1
    box = srs.next_box(old_box, correct) if row else (2 if correct else 1)
    due = srs.next_due(box, today).isoformat()
    conn.execute(
        """INSERT INTO progress (german, box, due, right_count, wrong_count)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(german) DO UPDATE SET
               box = excluded.box,
               due = excluded.due,
               right_count = right_count + ?,
               wrong_count = wrong_count + ?""",
        (german, box, due, int(correct), int(not correct), int(correct), int(not correct)),
    )
    conn.commit()


def stats(conn):
    """Return (words practiced, total right, total wrong)."""
    row = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(right_count), 0), COALESCE(SUM(wrong_count), 0) FROM progress"
    ).fetchone()
    return row
