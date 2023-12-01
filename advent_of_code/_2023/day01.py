from __future__ import annotations

import functools
import re


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


NUMS = {str(n): i for i, n in enumerate(range(1, 10), start=1)}
STRS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

FWDS = NUMS | {s: i for i, s in enumerate(STRS, start=1)}
REVS = NUMS | {s[::-1]: i for i, s in enumerate(STRS, start=1)}

FWD_RE = re.compile("|".join(f"({n})" for n in FWDS))
REV_RE = re.compile("|".join(f"({n})" for n in REVS))


def first(m: re.Match[str] | None) -> str:
    assert m is not None
    return m.group(0)


def part2(filename: str) -> int:
    return sum(
        FWDS[first(FWD_RE.search(line))] * 10 + REVS[first(REV_RE.search(line[::-1]))]
        for line in parse(filename)
    )


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
