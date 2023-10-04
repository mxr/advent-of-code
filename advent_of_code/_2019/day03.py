from __future__ import annotations

import functools
from collections import UserDict
from collections.abc import Mapping
from enum import Enum
from typing import TypeVar


class Dir(Enum):
    U = 1
    R = 2
    D = 3
    L = 4

    @property
    def dx(self) -> int:
        return (self == Dir.R) - (self == Dir.L)

    @property
    def dy(self) -> int:
        return (self == Dir.D) - (self == Dir.U)


class Step:
    dir: Dir
    val: int

    def __init__(self, raw: str) -> None:
        self.dir, self.val = Dir[raw[0]], int(raw[1:])


T = TypeVar("T")
U = TypeVar("U")


class SetOnceDict(UserDict[T, U]):
    def __setitem__(self, key: T, item: U) -> None:
        if item not in self.data:
            super().__setitem__(key, item)


def parse(filename: str) -> tuple[tuple[Step, ...], tuple[Step, ...]]:
    with open(filename) as f:
        steps1 = tuple(Step(s) for s in next(f).split(","))
        steps2 = tuple(Step(s) for s in next(f).split(","))

    return steps1, steps2


def board(steps: tuple[Step, ...]) -> Mapping[tuple[int, int], int]:
    b = SetOnceDict[tuple[int, int], int]()
    t, cx, cy = 0, 0, 0
    for step in steps:
        if step.dir.dx:
            for _ in range(step.val):
                cx += step.dir.dx
                t += 1
                b[cx, cy] = t
        if step.dir.dy:
            for _ in range(step.val):
                cy += step.dir.dy
                t += 1
                b[cx, cy] = t

    return b


@functools.cache
def boards(
    filename: str,
) -> tuple[Mapping[tuple[int, int], int], Mapping[tuple[int, int], int]]:
    steps1, steps2 = parse(filename)
    return board(steps1), board(steps2)


def part1(filename: str) -> int:
    board1, board2 = boards(filename)

    overlap = set(board1).intersection(board2)

    return min(abs(x) + abs(y) for x, y in overlap)


def part2(filename: str) -> int:
    board1, board2 = boards(filename)

    overlap = set(board1).intersection(board2)

    return min(board1[xy] + board2[xy] for xy in overlap)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
