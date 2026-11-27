"""German A1 Trainer. Terminal app with units, spaced repetition and saved progress."""
import random
from datetime import date

import db
import srs
from words import UNITS


def label(word):
    """Show a word with its article, e.g. 'der Tisch'."""
    german, _english, _arabic, article = word
    return f"{article} {german}".strip()


def is_correct(answer, word):
    """Accept the word with or without the article, in any letter case."""
    answer = answer.strip().lower()
    return answer in (word[0].lower(), label(word).lower())


def due_words(conn, unit_words, today):
    """Words from the unit that should be practiced now."""
    return [w for w in unit_words if srs.is_due(db.get_due_text(conn, w[0]), today)]


def choose_unit():
    names = list(UNITS)
    print("\nChoose a unit:")
    for i, name in enumerate(names, start=1):
        print(f"{i}. {name} ({len(UNITS[name])} words)")
    print(f"{len(names) + 1}. All units")
    choice = input("> ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        return UNITS[names[int(choice) - 1]]
    return [w for words in UNITS.values() for w in words]


def practice(conn):
    """Quiz on the words that are due, and save every answer."""
    today = date.today()
    words = due_words(conn, choose_unit(), today)
    if not words:
        print("\nNothing due here. Come back tomorrow!")
        return
    random.shuffle(words)
    words = words[:10]
    score = 0
    for word in words:
        answer = input(f"\nGerman for '{word[1]}' ({word[2]})? ")
        ok = is_correct(answer, word)
        db.record_answer(conn, word[0], ok, today)
        if ok:
            score += 1
            print("Richtig!")
        else:
            print(f"Falsch. It is: {label(word)}")
    print(f"\nScore: {score}/{len(words)}")


def flashcards():
    words = choose_unit()[:]
    random.shuffle(words)
    for word in words:
        print("\n" + label(word))
        if input("Enter = meaning, q = back: ").strip().lower() == "q":
            return
        print(f"  {word[1]}  |  {word[2]}")


def show_stats(conn):
    practiced, right, wrong = db.stats(conn)
    total = sum(len(w) for w in UNITS.values())
    print(f"\nWords practiced: {practiced}/{total}")
    print(f"Right answers: {right}, wrong answers: {wrong}")


def main():
    conn = db.connect()
    actions = {
        "1": ("Practice (spaced repetition)", lambda: practice(conn)),
        "2": ("Flashcards", flashcards),
        "3": ("My progress", lambda: show_stats(conn)),
    }
    while True:
        print("\n=== German A1 Trainer ===")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")
        print("q. Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            print("Tschüss!")
            return
        if choice in actions:
            actions[choice][1]()


if __name__ == "__main__":
    main()
