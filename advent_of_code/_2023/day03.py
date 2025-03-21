from __future__ import annotations

import functools
import itertools
import math
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@functools.cache
def parse(filename: str) -> tuple[dict[tuple[int, int], str], list[tuple[int, int]]]:
    with open(filename) as f:
        engine = defaultdict(lambda: ".")
        parts = []

        for row, line in enumerate(f):
            for col, c in enumerate(line.strip()):
                engine[row, col] = c
                if not ("0" <= c <= "9") and c != ".":
                    parts.append((row, col))

    return engine, parts


def neighbors(row: int, col: int) -> Generator[tuple[int, int]]:
    for r in (-1, 0, 1):
        for c in (-1, 0, 1):
            if r or c:
                yield row + r, col + c


def part1(filename: str) -> int:
    engine, parts = parse(filename)

    part_neighbors = set(
        itertools.chain.from_iterable(neighbors(row, col) for row, col in parts)
    )
    mrow = max(r for r, _ in engine) + 1
    mcol = max(c for _, c in engine) + 1

    total = 0
    for row in range(mrow):
        locs = []
        for col in range(mcol + 1):
            if "0" <= engine[row, col] <= "9":
                locs.append((row, col))
                continue

            if not part_neighbors.isdisjoint(locs):
                total += int("".join(engine[loc] for loc in locs))
            locs = []

    return total


def part2(filename: str) -> int:
    engine, parts = parse(filename)

    total = 0
    for row, col in parts:
        if engine[row, col] != "*":
            continue

        all_locs = set()
        for nr, nc in neighbors(row, col):
            if not "0" <= engine[nr, nc] <= "9":
                continue

            while "0" <= engine[nr, nc] <= "9":
                nc -= 1
            nc += 1
            sc = nc
            while "0" <= engine[nr, nc] <= "9":
                nc += 1
            all_locs.add(tuple((nr, c) for c in range(sc, nc)))

        if len(all_locs) != 2:
            continue

        total += math.prod(
            int("".join(engine[loc] for loc in locs)) for locs in all_locs
        )

    return total


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
