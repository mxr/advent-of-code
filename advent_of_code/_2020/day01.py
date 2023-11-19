from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for raw in f:
            yield int(raw)


def find(nums: list[int], target: int) -> tuple[int, int]:
    mapping = {target - n: n for n in nums}
    for n1, n2 in mapping.items():
        if n2 in mapping:
            return n1, n2

    return 0, 0


def part1(filename: str) -> int:
    n1, n2 = find(list(parse(filename)), 2020)

    return n1 * n2


def part2(filename: str) -> int:
    nums = list(parse(filename))
    for i, n in enumerate(nums):
        n1 = 2020 - n
        n2, n3 = find(nums[:i] + nums[i + 1 :], n1)
        if n + n2 + n3 == 2020:
            return n * n2 * n3

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
