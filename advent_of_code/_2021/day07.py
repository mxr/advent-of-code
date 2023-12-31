from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def parse(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(f) for f in f.read().split(",")]


def part1(filename: str) -> int:
    return execute(filename, fuel_part1)


def part2(filename: str) -> int:
    return execute(filename, fuel_part2)


def execute(filename: str, fuel_func: Callable[[int, int], int]) -> int:
    crabs = parse(filename)
    min_fuel = sum(fuel_func(c, 0) for c in crabs)
    for i in range(1, max(crabs)):
        m = 0
        for c in crabs:
            m += fuel_func(c, i)
            if m > min_fuel:
                break
        else:
            min_fuel = m

    return min_fuel


def fuel_part1(crab: int, i: int) -> int:
    return abs(crab - i)


def fuel_part2(crab: int, i: int) -> int:
    n = abs(crab - i)
    return n * (n + 1) // 2


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
