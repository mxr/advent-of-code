from __future__ import annotations

import functools
import itertools
import sys
from typing import cast


@functools.cache
def parse(
    filename: str,
) -> tuple[tuple[int, ...], dict[str, tuple[str, tuple[tuple[int, int, int], ...]]]]:
    with open(filename) as f:
        rseeds, *chunks = f.read().split("\n\n")

        seeds = tuple(int(n) for n in rseeds.removeprefix("seeds: ").split())

        maps = {}
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
    # convert ranges using mapping, adapted from reddit
    seeds, mappings = parse(filename)
    m = sys.maxsize
    for seed in itertools.batched(seeds, 2):
        ranges = [cast(tuple[int, int], seed)]
        curr = "seed"
        while curr != "location":
            nxt, vals = mappings[curr]
            new_ranges = []
            while ranges:
                rs, rl = ranges.pop()
                for drs, srs, srl in vals:
                    # overlap check - https://stackoverflow.com/a/3269471
                    if rs >= srs + srl or srs >= rs + rl:
                        continue
                    # remove LHS leftover from conversion
                    if rs < srs:
                        ranges.append((rs, srs - rs))
                        rs = srs
                    # remove RHS leftover from conversion
                    if srs + srl < rs + rl:
                        ranges.append((srs + srl, rs + rl - srs - srl))
                        rl = srs + srl - rs
                    new_ranges.append((rs + drs - srs, rl))
                    break
                else:
                    new_ranges.append((rs, rl))
            ranges, new_ranges = new_ranges, []
            curr = nxt
        m = min(m, min(ranges)[0])

    return m


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
