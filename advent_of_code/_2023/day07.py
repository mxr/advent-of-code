from __future__ import annotations

import functools
from collections import Counter
from typing import cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

STRENGTHS_P1 = {
    s: i
    for i, s in enumerate(
        reversed(("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"))
    )
}

STRENGTHS_P2 = {
    s: i
    for i, s in enumerate(
        reversed(("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"))
    )
}

TYPES = {
    t: i
    for i, t in enumerate(
        reversed(("FIVE", "FOUR", "FULL", "THREE", "TWO", "ONE", "HIGH"))
    )
}


def mctype(mc: list[tuple[str, int]]) -> str:
    if len(mc) == 1:
        return "FIVE"
    (_, c1), (_, c2), *_ = mc
    if c1 == 4:
        return "FOUR"
    if c1 == 3:
        return "FULL" if c2 == 2 else "THREE"
    if c1 == 2:
        return "TWO" if c2 == 2 else "ONE"
    return "HIGH"


@functools.cache
def key_part1(hand: str) -> tuple[int, int, int, int, int, int]:
    typ = TYPES[mctype(Counter(hand).most_common())]

    strengths = cast(
        tuple[int, int, int, int, int], tuple(STRENGTHS_P1[c] for c in hand)
    )

    return typ, *strengths


@functools.cache
def key_part2(hand: str) -> tuple[int, int, int, int, int, int]:
    def mctype_part2() -> str:
        c = Counter(hand)
        mc = c.most_common()
        if "J" not in c:
            return mctype(mc)

        mc.remove(("J", c["J"]))
        if not mc:
            return "FIVE"

        mc[0] = (mc[0][0], mc[0][1] + c["J"])

        return mctype(mc)

    strengths = cast(
        tuple[int, int, int, int, int], tuple(STRENGTHS_P2[c] for c in hand)
    )

    return TYPES[mctype_part2()], *strengths


@functools.cache
def parse(filename: str) -> tuple[tuple[str, int], ...]:
    def gen() -> Generator[tuple[str, int], None, None]:
        with open(filename) as f:
            for line in f:
                card, _, rbid = line.partition(" ")
                yield card, int(rbid)

    return tuple(gen())


def part1(filename: str) -> int:
    return sum(
        i * bid
        for i, (_, bid) in enumerate(
            sorted((key_part1(hand), bid) for hand, bid in parse(filename)), start=1
        )
    )


def part2(filename: str) -> int:
    return sum(
        i * bid
        for i, (_, bid) in enumerate(
            sorted((key_part2(hand), bid) for hand, bid in parse(filename)), start=1
        )
    )


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))