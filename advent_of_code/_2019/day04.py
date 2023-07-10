from __future__ import annotations

import functools
from collections import Counter
from collections.abc import Iterator
from itertools import tee


@functools.cache
def parse(filename: str) -> tuple[int, int]:
    with open(filename) as f:
        rl, _, rh = f.read().partition("-")
    return int(rl), int(rh)


def pairs(digits: str) -> tuple[Iterator[str], Iterator[str]]:
    first, second = tee(digits)
    next(second)

    return first, second


def part1(filename: str) -> int:
    lo, hi = parse(filename)

    total = 0
    for n in range(lo, hi + 1):
        digits = str(n)

        total += any(int(f) == int(s) for f, s in zip(*pairs(digits))) and all(
            int(f) <= int(s) for f, s in zip(*pairs(digits))
        )

    return total


def part2(filename: str) -> int:
    lo, hi = parse(filename)

    total = 0
    for n in range(lo, hi + 1):
        digits = str(n)

        total += (2 in Counter(digits).values()) and all(
            int(f) <= int(s) for f, s in zip(*pairs(digits))
        )

    return total


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
