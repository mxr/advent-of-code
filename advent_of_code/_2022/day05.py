from __future__ import annotations

import functools
import re
from itertools import zip_longest

RE = re.compile(r"\d+")
SKIP = frozenset(("[", "]", " "))


@functools.cache
def parse(filename: str) -> tuple[list[tuple[str, ...]], list[tuple[int, int, int]]]:
    with open(filename) as f:
        positions, instructions = f.read().split("\n\n")

    cols = tuple(
        zip_longest(*tuple(tuple(s) for s in positions.splitlines()), fillvalue=" ")
    )

    i = 1
    initial_stacks = []
    while i < len(cols):
        col = cols[i]
        initial_stacks.append(
            tuple(col[i] for i in range(len(col) - 2, -1, -1) if col[i] not in SKIP)
        )
        i += 4

    nums = []
    for instr in instructions.splitlines():
        m = RE.findall(instr)
        assert len(m) == 3, (m, instr)

        amt, s1, s2 = int(m[0]), int(m[1]) - 1, int(m[2]) - 1
        nums.append((amt, s1, s2))

    return initial_stacks, nums


def part1(filename: str) -> int:
    initial_stacks, nums = parse(filename)
    stacks = [list(s) for s in initial_stacks]

    for amt, s1, s2 in nums:
        stacks[s1], top = stacks[s1][:-amt], reversed(stacks[s1][-amt:])
        stacks[s2].extend(top)

    print("".join(s[-1] for s in stacks), end=" ")
    return -1


def part2(filename: str) -> int:
    initial_stacks, nums = parse(filename)
    stacks = [list(s) for s in initial_stacks]

    for amt, s1, s2 in nums:
        stacks[s1], top = stacks[s1][:-amt], stacks[s1][-amt:]
        stacks[s2].extend(top)

    print("".join(s[-1] for s in stacks), end=" ")
    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
