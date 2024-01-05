from __future__ import annotations

import bisect
import functools
import itertools


@functools.cache
def parse(filename: str) -> tuple[tuple[str, ...], ...]:
    with open(filename) as f:
        return tuple(tuple(line.strip()) for line in f)


def part1(filename: str) -> int:
    return sum_dists(parse(filename), 2)


def part2(filename: str) -> int:
    return sum_dists(parse(filename), 1000000)


def sum_dists(universe: tuple[tuple[str, ...], ...], mult: int) -> int:
    empty_rows = tuple(
        r for r, row in enumerate(universe) if all(cell == "." for cell in row)
    )
    empty_cols = tuple(
        c for c in range(len(universe[0])) if all(row[c] == "." for row in universe)
    )

    galaxies = (
        (r, c)
        for r, row in enumerate(universe)
        for c, cell in enumerate(row)
        if cell == "#"
    )

    return sum(
        (abs(r1 - r2) + abs(c1 - c2))
        + dist_mult(r1, r2, mult, empty_rows)
        + dist_mult(c1, c2, mult, empty_cols)
        for (r1, c1), (r2, c2) in itertools.combinations(galaxies, 2)
    )


def dist_mult(p1: int, p2: int, m: int, e: tuple[int, ...]) -> int:
    pmin, pmax = (p1, p2) if p1 < p2 else (p2, p1)
    return (m - 1) * len(e[bisect.bisect_left(e, pmin) : bisect.bisect(e, pmax)])


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
