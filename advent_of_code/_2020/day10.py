from __future__ import annotations

import functools
from collections import Counter
from collections.abc import Generator


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1(filename: str) -> int:
    nums = [0]  # outlet
    nums.extend(sorted(parse(filename)))
    nums.append(nums[-1] + 3)  # device

    diffs = (nums[i + 1] - nums[i] for i in range(len(nums) - 1))
    counts = Counter(diffs)

    return counts[1] * counts[3]


def part2(filename: str) -> int:
    nums = [0]  # outlet
    nums.extend(sorted(parse(filename)))
    nums.append(nums[-1] + 3)  # device

    @functools.lru_cache(len(nums))
    def count_ways(i: int) -> int:
        if i == len(nums) - 1:
            return 1
        return sum(
            count_ways(j)
            for j in (i + 1, i + 2, i + 3)
            if j < len(nums) and nums[j] - nums[i] <= 3
        )

    return count_ways(0)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
