from __future__ import annotations

from collections import defaultdict
from itertools import product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class Cubes:
    def __init__(self, section: list[str], dims: int) -> None:
        assert dims >= 3

        self.cubes: dict[tuple[int, ...], str] = defaultdict(lambda: ".")
        self.deltas = frozenset(product((-1, 0, 1), repeat=dims)) - {(0,) * dims}
        self.extras = dims - 2

        self.height, self.width, self.depth = len(section), len(section[0]), 0
        for i, line in enumerate(section):
            for j, c in enumerate(line):
                self.cubes[(i, j, *(0,) * self.extras)] = c

    def cycle(self) -> None:
        new_cubes = self.cubes.copy()

        # "all cubes simultaneously change their state"
        # but because state depends on neighbors we can look at a bit
        # beyond the known cubes
        for x in range(self.width // 2 - self.width, self.width // 2 + self.width + 1):
            for y in range(
                self.height // 2 - self.height, self.height // 2 + self.height + 1
            ):
                for zs in product(
                    range(-self.depth - 2, self.depth + 2 + 1), repeat=self.extras
                ):
                    k = x, y, *zs

                    num_active = 0
                    for neighbor in self._neighbors(*k):
                        num_active += neighbor == "#"
                        if num_active > 3:
                            break

                    active = self.cubes[k] == "#"
                    if active and (num_active != 2 and num_active != 3):
                        new_cubes[k] = "."
                    elif not active and num_active == 3:
                        new_cubes[k] = "#"

        self.width += 2
        self.height += 2
        self.depth += 2

        self.cubes = new_cubes

    def count(self) -> int:
        return sum(c == "#" for c in self.cubes.values())

    def _neighbors(self, x: int, y: int, *zs: int) -> Generator[str, None, None]:
        for xd, yd, *zds in self.deltas:
            yield self.cubes[
                (x + xd, y + yd, *(z + zd for z, zd in zip(zs, zds, strict=True)))
            ]


def parse(filename: str, dims: int) -> Cubes:
    with open(filename) as f:
        cubes = Cubes(f.read().splitlines(), dims)

    return cubes


def execute(filename: str, dims: int) -> int:
    cubes = parse(filename, dims)
    for _ in range(6):
        cubes.cycle()
    return cubes.count()


def part1(filename: str) -> int:
    return execute(filename, 3)


def part2(filename: str) -> int:
    return execute(filename, 4)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
