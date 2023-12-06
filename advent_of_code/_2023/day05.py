from __future__ import annotations

import functools
from typing import cast


@functools.cache
def parse(
    filename: str,
) -> tuple[tuple[int, ...], dict[str, tuple[str, tuple[tuple[int, int, int], ...]]]]:
    with open(filename) as f:
        seeds = tuple(int(n) for n in next(f).removeprefix("seeds: ").split())
        next(f)

        maps = {}
        chunks = f.read().split("\n\n")
        for chunk in chunks:
            title, *rnums = chunk.splitlines()
            src, _, dst = title.removesuffix(" map:").partition("-to-")
            mappings = tuple(
                sorted(
                    (
                        cast(tuple[int, int, int], tuple(int(rn) for rn in rns.split()))
                        for rns in rnums
                    ),
                    key=lambda ns: ns[1],
                )
            )

            maps[src] = (dst, mappings)

    return seeds, maps


def location(
    val: int, mappings: dict[str, tuple[str, tuple[tuple[int, int, int], ...]]]
) -> int:
    curr = "seed"
    while curr != "location":
        nxt, vals = mappings[curr]
        for drs, srs, rl in vals:
            if srs <= val < srs + rl:
                val = val - srs + drs
                break
        curr = nxt

    return val


def part1(filename: str) -> int:
    seeds, mappings = parse(filename)

    return min(location(s, mappings) for s in seeds)


def part2(filename: str) -> int:
    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
