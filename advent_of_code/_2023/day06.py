from __future__ import annotations

import functools
import itertools
import re

RE = re.compile(r"\d+")


@functools.cache
def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        return tuple(int(m.group()) for m in RE.finditer(f.read()))


def race(n: int, t: int, d: int) -> bool:
    return n * (t - n) > d


def part1(filename: str) -> int:
    p = 1

    ts, ds = itertools.batched(ns := parse(filename), len(ns) // 2, strict=True)
    for t, d in zip(ts, ds, strict=True):
        wins = 0
        for n in range(1, t):
            if race(n, t, d):
                wins += 1
            elif wins:
                break
        p *= wins

    return p


def part2(filename: str) -> int:
    ns = parse(filename)
    t, d = (
        int("".join(str(n) for n in ds))
        for ds in itertools.batched(ns, len(ns) // 2, strict=True)
    )

    # binsearch from https://stackoverflow.com/a/38058945

    # assume first occurrence of win is in first half
    s = -1
    lo, hi = 1, t // 2
    while lo <= hi:
        m = (hi + lo) // 2
        if race(m, t, d):
            s = m
            hi = m - 1
        else:
            lo = m + 1

    # assume last occurrence of win is in last half
    e = -1
    lo, hi = t // 2 + 1, t - 1
    while lo <= hi:
        m = (hi + lo) // 2
        if not race(m, t, d):
            e = m - 1
            hi = m - 1
        else:
            lo = m + 1

    return e - s + 1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
