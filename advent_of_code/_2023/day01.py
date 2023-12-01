from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import TypeGuard, Optional

@functools.cache
def parse(filename: str) -> tuple[str, ...]:
    with open(filename) as f:
        return tuple(f.read().splitlines())


def part1(filename: str) -> int:
    return sum(
        (
            next(int(c) * 10 for c in line if "0" <= c <= "9")
            + next(int(c) for c in reversed(line) if "0" <= c <= "9")
        )
        for line in parse(filename)
    )


NUMS = {str(n): i + 1 for i, n in enumerate(range(1,10)}
STRS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

FWDS = NUMS| {    s: i + 1 for i, s in enumerate(STRS)}
REVS = NUMS | {    s[::-1]: i + 1 for i, s in enumerate(STRS)}

FWD_RE = re.compile("|".join(f"({n})" for n in FWDS))
REV_RE = re.compile("|".join(f"({n})" for n in REVS))

def must(x: Optional[T])->TypeGuard[T]:
    assert x is not None

def part2(filename: str) -> int:
    total = 0
    for line in parse(filename):
        tens = FWDS[must(FWD_RE.search(line)).group(0)]
        ones = REVS[m.group(0)] if (m := REV_RE.search(line[::-1])) else tens
        total += tens * 10 + ones

    return total


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
