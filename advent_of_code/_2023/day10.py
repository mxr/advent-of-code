from __future__ import annotations

import functools
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@functools.cache
def parse(filename: str) -> tuple[tuple[str, ...], ...]:
    def gen() -> Generator[tuple[str, ...], None, None]:
        with open(filename) as f:
            for line in f:
                yield tuple(line.rstrip())

    return tuple(gen())


class Dir(Enum):
    N = 1
    E = 2
    S = 3
    W = 4


@functools.cache
def traverse(
    b: tuple[tuple[str, ...], ...],
) -> list[tuple[int, int]]:
    sr, sc = next(
        (r, c) for r, row in enumerate(b) for c, cell in enumerate(row) if cell == "S"
    )

    snr, snc = next(
        (r, c)
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0))
        if 0 <= (r := sr + dr) < len(b)
        and 0 <= (c := sc + dc) < len(b[0])
        and (
            (b[r][c] == "|" and dr)
            or (b[r][c] == "-" and dc)
            or (b[r][c] == "L" and (dr == 1 or dc == -1))
            or (b[r][c] == "J" and (dr == 1 or dc == 1))
            or (b[r][c] == "7" and (dr == -1 or dc == 1))
            or (b[r][c] == "F" and (dr == -1 or dc == -1))
        )
    )

    sd = (Dir.N if snr < sr else Dir.S) if sc == snc else (Dir.W if snc < sc else Dir.E)

    d, r, c = sd, snr, snc
    loop = [(sr, sc)]
    while (t := b[r][c]) != "S":
        loop.append((r, c))
        if t == "|":
            r += -1 if d == Dir.N else 1
        elif t == "-":
            c += -1 if d == Dir.W else 1
        elif t == "L":
            if d == Dir.S:
                c, d = c + 1, Dir.E
            else:
                r, d = r - 1, Dir.N
        elif t == "J":
            if d == Dir.S:
                c, d = c - 1, Dir.W
            else:
                r, d = r - 1, Dir.N
        elif t == "7":
            if d == Dir.N:
                c, d = c - 1, Dir.W
            else:
                r, d = r + 1, Dir.S
        else:
            assert t == "F"
            if d == Dir.N:
                c, d = c + 1, Dir.E
            else:
                r, d = r + 1, Dir.S

    return loop


def part1(filename: str) -> int:
    b = parse(filename)

    return len(traverse(b)) // 2


def part2(filename: str) -> int:
    b = parse(filename)

    loop = traverse(b)

    # adapted from reddit
    # gaussian formula (shoelace theorem) minus the area added by the loop itself
    a2 = 0
    for i, (r1, c1) in enumerate(loop):
        r2, c2 = loop[(i + 1) % len(loop)]
        a2 += (c1 + c2) * (r2 - r1)
    return (abs(a2) - len(loop)) // 2 + 1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
