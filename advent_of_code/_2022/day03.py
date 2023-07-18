from __future__ import annotations

import functools
from collections.abc import Generator


@functools.cache
def parse(filename: str) -> tuple[str, ...]:
    def gen() -> Generator[str, None, None]:
        with open(filename) as f:
            for line in f:
                yield line.strip()

    return tuple(gen())


def part1(filename: str) -> int:
    def common() -> Generator[str, None, None]:
        for r in parse(filename):
            m = len(r) // 2
            yield (set(r[:m]) & set(r[m:])).pop()

    return sum(ord(c) - (96 if "a" <= c <= "z" else 38) for c in common())


def part2(filename: str) -> int:
    def common() -> Generator[str, None, None]:
        i = 0
        rucksacks = parse(filename)
        while i < len(rucksacks):
            r1, r2, r3 = rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]
            yield (set(r1) & set(r2) & set(r3)).pop()
            i += 3

    return sum(ord(c) - (96 if "a" <= c <= "z" else 38) for c in common())


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
