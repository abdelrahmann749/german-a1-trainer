# German A1 Trainer

A small command line app I wrote to learn German vocabulary for my A1 level. I'm preparing for an Ausbildung in Germany, so I use it every day.

You pick a unit, the app asks you the words, and it remembers which ones you got wrong. Those come back sooner than the ones you already know.

## What it does

- 5 units with 53 A1 words (with der/die/das, English and Arabic)
- Practice mode with spaced repetition (Leitner boxes)
- Progress is saved in a SQLite file, so it is still there tomorrow
- Flashcards and a progress screen
- Unit tests for the main logic

## How to run it

You need Python 3.8 or newer. There is nothing to install.

    python main.py

To run the tests:

    python -m unittest -v

## How the repetition works

Every word is in a box from 1 to 5.

- Right answer: the word moves up one box.
- Wrong answer: the word goes back to box 1.

The higher the box, the longer the app waits before asking again: 1, 2, 4, 8 and 16 days for boxes 1 to 5. A word you never practiced is always due.

## Files

| File | What it does |
| --- | --- |
| `main.py` | the menu and the questions in the terminal |
| `srs.py` | the box rules and the due dates |
| `db.py` | reads and writes the progress in SQLite |
| `words.py` | the words, split into units |
| `test_trainer.py` | the tests |
| `CODE_GUIDE_AR.md` | notes about the code in Arabic |

## Adding words

Open `words.py` and add a line to a unit:

    ("Fenster", "window", "شباك", "das"),

The last value is the article. Leave it empty (`""`) for verbs and adjectives.

## To do

- Web version (maybe Flask)
- More units, and A2 words
