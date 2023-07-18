from __future__ import annotations

from collections import deque


def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def helper(filename: str, n: int) -> int:
    d: deque[str] = deque()
    for i, c in enumerate(parse(filename)):
        d.append(c)

        if len(d) < n:
            continue
        if len(d) == len(set(d)):
            return i + 1

        d.popleft()

    return -1


def part1(filename: str) -> int:
    return helper(filename, 4)


def part2(filename: str) -> int:
    return helper(filename, 14)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
