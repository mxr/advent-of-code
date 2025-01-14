from __future__ import annotations

import functools
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@functools.cache
def parse(filename: str) -> tuple[tuple[int, int], ...]:
    def gen() -> Generator[tuple[int, int]]:
        with open(filename) as f:
            for line in f:
                card, _, rnums = line.partition(":")
                rwin, _, rhave = rnums.partition("|")

                wins = tuple(int(n) for n in rwin.split())
                have = tuple(int(n) for n in rhave.split())

                yield (
                    int(card.removeprefix("Card ")),
                    len(set(wins).intersection(have)),
                )

    return tuple(gen())


def part1(filename: str) -> int:
    return sum(2 ** (p - 1) if p else 0 for _, p in parse(filename))


def part2(filename: str) -> int:
    counts: Counter[int] = Counter()
    for c, p in parse(filename):
        counts[c] += 1
        for i in range(c + 1, c + p + 1):
            counts[i] += counts[c]

    return sum(counts.values())


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
