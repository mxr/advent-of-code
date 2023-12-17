from __future__ import annotations

import functools
import math
import re

RE = re.compile(r"\w+")


@functools.cache
def parse(filename: str) -> tuple[str, dict[str, tuple[str, str]]]:
    with open(filename) as f:
        instrs, _, *rest = f.read().splitlines()

    d = {}
    for r in rest:
        s, lt, rt = RE.findall(r)
        d[s] = lt, rt

    return instrs, d


def part1(filename: str) -> int:
    instrs, d = parse(filename)

    n = 0
    curr = "AAA"
    while curr != "ZZZ":
        curr = d[curr][int(instrs[n % len(instrs)] == "R")]
        n += 1

    return n


def part2(filename: str) -> int:
    instrs, d = parse(filename)

    ns = []
    for start in d:
        if not start.endswith("A"):
            continue

        n = 0
        curr = start
        while not curr.endswith("Z"):
            curr = d[curr][int(instrs[n % len(instrs)] == "R")]
            n += 1

        ns.append(n)

    return math.lcm(*ns)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
