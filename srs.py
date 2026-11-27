"""Spaced repetition with Leitner boxes. Only simple functions here, no database.

A word sits in a box from 1 to 5.
- Right answer: it moves up one box, so you see it less often.
- Wrong answer: it goes back to box 1, so you see it tomorrow.
"""
from datetime import date, timedelta

MAX_BOX = 5
# Days to wait before seeing the word again, by box.
DAYS_BY_BOX = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}


def next_box(box, correct):
    """Return the new box after an answer."""
    if correct:
        return min(box + 1, MAX_BOX)
    return 1


def next_due(box, today):
    """Return the date when a word in this box should be asked again."""
    return today + timedelta(days=DAYS_BY_BOX[box])


def is_due(due_text, today):
    """A word is due if it has never been seen (None) or its date has come."""
    if due_text is None:
        return True
    return date.fromisoformat(due_text) <= today
