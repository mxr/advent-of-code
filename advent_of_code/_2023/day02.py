from __future__ import annotations

import functools
import math
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

RE_RED = re.compile(r"(\d+) red")
RE_GREEN = re.compile(r"(\d+) green")
RE_BLUE = re.compile(r"(\d+) blue")


def mtoi(m: re.Match[str] | None) -> int:
    assert m is not None
    return int(m.group())


@functools.cache
def parse(filename: str) -> tuple[tuple[int, tuple[tuple[int, int, int], ...]], ...]:
    def gen() -> Generator[tuple[int, tuple[tuple[int, int, int], ...]], None, None]:
        with open(filename) as f:
            for line in f:
                game, rounds = line.split(":")

                n = int(game.removeprefix("Game "))

                cnts = tuple(
                    (
                        int(m.group(1)) if (m := RE_RED.search(rnd)) else 0,
                        int(m.group(1)) if (m := RE_GREEN.search(rnd)) else 0,
                        int(m.group(1)) if (m := RE_BLUE.search(rnd)) else 0,
                    )
                    for rnd in rounds.split(";")
                )

                yield n, cnts

    return tuple(gen())


def part1(filename: str) -> int:
    target = (12, 13, 14)

    return sum(
        n
        for n, cnts in parse(filename)
        if all(c <= t for cnt in cnts for c, t in zip(cnt, target, strict=True))
    )


def part2(filename: str) -> int:
    return sum(
        math.prod(max(c) for c in zip(*cnts, strict=True))
        for _, cnts in parse(filename)
    )


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
