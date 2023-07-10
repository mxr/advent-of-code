from __future__ import annotations

from collections import Counter


def parse(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(n) for n in f.read().split(",")]


def execute(filename: str, day: int) -> int:
    starting = parse(filename)

    turns = {n: i + 1 for i, n in enumerate(starting)}
    spoken = Counter(starting)

    prev, curr = starting[-1], -1
    curr = -1
    for i in range(len(starting) + 1, day + 1):
        curr = (i - 1) - turns[prev] if spoken[prev] > 1 else 0

        turns[prev] = i - 1
        spoken[curr] += 1
        prev = curr

    return curr


def part1(filename: str) -> int:
    return execute(filename, 2020)


def part2(filename: str) -> int:
    return execute(filename, 30000000)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
