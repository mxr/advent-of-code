from __future__ import annotations

import functools


@functools.cache
def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        return tuple(int(line) for line in f)


def fuel(mass: int) -> int:
    return int(mass / 3 - 2)


def part1(filename: str) -> int:
    return sum(fuel(m) for m in parse(filename))


def part2(filename: str) -> int:
    total = 0
    for mass in parse(filename):
        this_fuel = fuel(mass)
        while this_fuel >= 0:
            total += this_fuel
            this_fuel = fuel(this_fuel)

    return total


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
