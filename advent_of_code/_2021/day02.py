from __future__ import annotations

from typing import NamedTuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class Vector(NamedTuple):
    direction: str
    value: int


def parse(filename: str) -> Generator[Vector]:
    with open(filename) as f:
        for line in f:
            p1, _, p2 = line.partition(" ")
            yield Vector(p1, int(p2))


def part1(filename: str) -> int:
    hor, ver = 0, 0

    for v in parse(filename):
        if v.direction == "forward":
            hor += v.value
        elif v.direction == "down":
            ver += v.value
        else:
            ver -= v.value

    return hor * ver


def part2(filename: str) -> int:
    hor, ver, aim = 0, 0, 0

    for v in parse(filename):
        if v.direction == "forward":
            hor += v.value
            ver += aim * v.value
        elif v.direction == "down":
            aim += v.value
        else:
            aim -= v.value

    return hor * ver


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
