from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

RE = re.compile(r"\d+")


@functools.cache
def parse(filename: str) -> tuple[tuple[int, int, int, int], ...]:
    def gen() -> Generator[tuple[int, int, int, int]]:
        with open(filename) as f:
            for line in f.readlines():
                m = RE.findall(line)
                assert len(m) == 4, (m, line)

                yield int(m[0]), int(m[1]), int(m[2]), int(m[3])

    return tuple(gen())


def part1(filename: str) -> int:
    return sum(
        n1 <= n3 <= n4 <= n2 or n3 <= n1 <= n2 <= n4
        for n1, n2, n3, n4 in parse(filename)
    )


def part2(filename: str) -> int:
    return sum(n1 <= n3 <= n2 or n3 <= n1 <= n4 for n1, n2, n3, n4 in parse(filename))


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
