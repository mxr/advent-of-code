from __future__ import annotations

import functools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


RE = re.compile("#+")


@functools.cache
def parse(filename: str) -> tuple[tuple[str, tuple[int, ...]], ...]:
    def gen() -> Generator[tuple[str, tuple[int, ...]], None, None]:
        with open(filename) as solve:
            for line in solve:
                springs, _, rnums = line.partition(" ")
                yield springs, tuple(int(rn) for rn in rnums.split(","))

    return tuple(gen())


def part1(filename: str) -> int:
    return sum(
        tuple(len(m.group()) for m in RE.finditer(way)) == ns
        for s, ns in parse(filename)
        for way in ways(s)
    )


@functools.cache
def ways(s: str) -> tuple[str, ...]:
    if not s:
        return ("",)

    p = s.find("?")
    if p == -1:
        return (s,)

    return tuple(s[:p] + c + r for c in (".", "#") for r in ways(s[p + 1 :]))


def part2(filename: str) -> int:
    return sum(numways2("?".join((s,) * 5), ns * 5) for s, ns in parse(filename))


# dp solution, inspired by reddit
def numways2(s: str, ns: tuple[int, ...]) -> int:
    memo: dict[tuple[int, int, int], int] = {}

    def solve(
        s: str,
        ns: tuple[int, ...],
        si: int,
        nsi: int,
        curlen: int,  # length of contiguous `#`
    ) -> int:
        key = (si, nsi, curlen)
        if key in memo:
            return memo[key]

        # end of string
        if si == len(s):
            return int(
                # off the end of nums with no more `#`
                (nsi == len(ns) and curlen == 0)
                # on the last num with exactly that many `#`
                or (nsi == len(ns) - 1 and ns[nsi] == curlen)
            )

        num = 0
        for c in (".", "#"):
            # check if cur char matches desired replacement (either doing no-op replacement
            # or replacing the question mark with two options)
            if s[si] != c and s[si] != "?":
                continue

            # contiguous `#` hasn't started yet
            if c == "." and curlen == 0:
                # check next character against rest of counts
                num += solve(s, ns, si + 1, nsi, 0)

            # end of contiguous `#` with matching count
            elif c == "." and curlen > 0 and nsi < len(ns) and ns[nsi] == curlen:
                # check rest of springs against rest of counts
                num += solve(s, ns, si + 1, nsi + 1, 0)

            # continuing contiguous `#`
            elif c == "#":
                # check next character against rest of counts & add this `#` to curlen
                num += solve(s, ns, si + 1, nsi, curlen + 1)

        memo[key] = num
        return num

    return solve(s, ns, 0, 0, 0)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
