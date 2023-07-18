from __future__ import annotations


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read()


# A for Rock, B for Paper, and C for Scissors.
# X for Rock, Y for Paper, and Z for Scissors
WIN = {"X": "C", "Y": "A", "Z": "B"}
DRAW = {
    "X": "A",
    "Y": "B",
    "Z": "C",
}

TO_WIN = {v: k for k, v in WIN.items()}
TO_DRAW = {v: k for k, v in DRAW.items()}
TO_LOSE = {
    "A": "Z",
    "B": "X",
    "C": "Y",
}

SCORES = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def win(you: str, opponent: str) -> bool:
    return WIN[you] == opponent


def draw(you: str, opponent: str) -> bool:
    return DRAW[you] == opponent


def force(opponent: str, outcome: str) -> str:
    if outcome == "X":
        return TO_LOSE[opponent]
    elif outcome == "Y":
        return TO_DRAW[opponent]
    else:
        return TO_WIN[opponent]


def part1(filename: str) -> int:
    inp = parse(filename).splitlines()

    score = 0
    for game in inp:
        opponent, _, you = game.partition(" ")
        score += SCORES[you]
        score += 6 if win(you, opponent) else 3 if draw(you, opponent) else 0

    return score


def part2(filename: str) -> int:
    inp = parse(filename).splitlines()

    score = 0
    for game in inp:
        opponent, _, outcome = game.partition(" ")
        you = force(opponent, outcome)
        score += SCORES[you]
        score += 6 if win(you, opponent) else 3 if draw(you, opponent) else 0

    return score


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
