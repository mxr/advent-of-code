from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Generator


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1(filename: str) -> int:
    nums = list(parse(filename))
    preamble = deque(nums[:25])
    for i in range(26, len(nums)):
        n = nums[i]
        m, *_ = find(preamble, n)
        if not m:
            return n

        preamble.popleft()
        preamble.append(n)

    return -1


def find(nums: Iterable[int], target: int) -> tuple[int, int]:
    mapping = {target - n: n for n in nums}
    for n1, n2 in mapping.items():
        if n2 in mapping:
            return n1, n2

    return 0, 0


def part2(filename: str) -> int:
    target = part1(filename)

    nums = list(parse(filename))

    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s > target:
                break
            elif s == target:
                return min(nums[i : j + 1]) + max(nums[i : j + 1])

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
