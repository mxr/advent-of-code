from __future__ import annotations

import functools
from itertools import batched

WIDTH = 25
HEIGHT = 6


@functools.cache
def parse(filename: str) -> str:
    with open(filename) as f:
        return f.read().strip()


def part1(filename: str) -> int:
    minlayer = min(
        batched(parse(filename), WIDTH * HEIGHT), key=lambda layer: layer.count("0")
    )

    return minlayer.count("1") * minlayer.count("2")


def part2(filename: str) -> int:
    layers = tuple(
        tuple(batched(layer, WIDTH))
        for layer in batched(parse(filename), WIDTH * HEIGHT)
    )

    out = [[" "] * WIDTH for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for layer in layers:
                if (c := layer[i][j]) != "2":
                    out[i][j] = "⬛️" if c == "0" else "⬜️"
                    break

    print()
    for row in out:
        print(*row, sep="")

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
