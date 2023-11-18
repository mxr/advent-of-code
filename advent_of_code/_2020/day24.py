from __future__ import annotations

import functools
from collections import Counter
from collections import defaultdict
from itertools import permutations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def parse(filename: str) -> Generator[Counter[str], None, None]:
    with open(filename) as f:
        for line in f:
            steps: Counter[str] = Counter()
            i = 0
            while i < len(line) - 1:
                if line[i] == "e" or line[i] == "w":
                    steps[line[i]] += 1
                    i += 1
                else:
                    steps[line[i : i + 2]] += 1
                    i += 2

            yield steps


def execute(filename: str, days: int) -> int:
    b = flip(filename)

    for _ in range(days):
        q = set(b)
        q.update(n for t in b for n in neighbors(*t))

        nb = b.copy()
        while q:
            t = q.pop()
            c = Counter(b[n] for n in neighbors(*t))
            if b[t] == "b" and (c["b"] == 0 or c["b"] > 2):
                nb[t] = "w"
            if b[t] == "w" and c["b"] == 2:
                nb[t] = "b"
        b = nb.copy()

    return sum(v == "b" for v in b.values())


DELTAS = tuple(permutations((-1, 0, 1), r=3))


def neighbors(q: int, r: int, s: int) -> Generator[tuple[int, int, int], None, None]:
    for qd, rd, sd in DELTAS:
        yield q + qd, r + rd, s + sd


@functools.lru_cache(maxsize=1)
def flip(filename: str) -> dict[tuple[int, int, int], str]:
    b: dict[tuple[int, int, int], str] = defaultdict(lambda: "w")

    for c in parse(filename):
        # https://archive.ph/CNIfX#coordinates-cube
        q, r, s = 0, 0, 0
        for d, i in c.items():
            if d == "e":
                q += i
                s -= i
            elif d == "se":
                r += i
                s -= i
            elif d == "sw":
                q -= i
                r += i
            elif d == "w":
                q -= i
                s += i
            elif d == "nw":
                r -= i
                s += i
            elif d == "ne":
                q += i
                r -= i
            else:
                raise ValueError(f"invalid direction {d}")
        b[q, r, s] = "b" if b[q, r, s] == "w" else "w"

    return b


def part1(filename: str) -> int:
    return execute(filename, 0)


def part2(filename: str) -> int:
    return execute(filename, 100)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
