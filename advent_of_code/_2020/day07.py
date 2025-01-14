from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

RE = re.compile(r"(\d+) (\w+ \w+) bags?")


def parse(filename: str) -> Generator[tuple[str, list[tuple[int, str]]]]:
    with open(filename) as f:
        for line in f.readlines():
            first, _, rest = line.partition(" contain ")
            outer = first[: -len(" bags")]
            inner = [(int(n), c) for (n, c) in RE.findall(rest)]
            yield outer, inner


def part1(filename: str) -> int:
    mapping = dict(parse(filename))
    can_contain = 0
    for start in mapping:
        q = [start]
        seen = set()
        while q:
            outer = q.pop()
            if outer in seen:
                continue
            seen.add(outer)
            if outer == "shiny gold":
                can_contain += 1
                break
            else:
                q.extend(color for _, color in mapping[outer])

    return can_contain - 1


def part2(filename: str) -> int:
    mapping = dict(parse(filename))

    @functools.lru_cache(len(mapping))
    def count_bags(color: str) -> int:
        if not mapping[color]:
            return 1
        return 1 + sum(n * count_bags(c) for n, c in mapping[color])

    return count_bags("shiny gold") - 1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
