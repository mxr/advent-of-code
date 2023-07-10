from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from itertools import cycle
from typing import NewType

SeatHash = NewType("SeatHash", tuple[tuple[str, ...], ...])


class Ferry:
    def __init__(self, seats: list[list[str]]):
        self.seats = seats
        self.height, self.width = len(self.seats), len(self.seats[0])
        self._seen: set[SeatHash] = {self._hash()}

    def sit(self, part: int) -> bool:
        if part == 1:
            neighbor_func, limit = self._neighbors, 4
        else:
            neighbor_func, limit = self._visible, 5

        deltas = []
        for i, row in enumerate(self.seats):
            for j, seat in enumerate(row):
                if seat == ".":
                    continue

                neighbors = neighbor_func(i, j)
                if seat == "L" and not any(n == "#" for n in neighbors):
                    deltas.append((i, j, "#"))
                elif seat == "#":
                    seen_other, seen_occupied = 0, 0
                    for n in neighbors:
                        if n == "#":
                            seen_occupied += 1
                        else:
                            seen_other += 1
                        if seen_occupied >= limit:
                            deltas.append((i, j, "L"))
                            break
                        if seen_other - seen_occupied > 8 - limit:
                            break

        for i, j, seat in deltas:
            self.seats[i][j] = seat

        h = self._hash()
        if h in self._seen:
            return True

        self._seen.add(h)
        return False

    def count(self) -> int:
        return sum(seat == "#" for row in self.seats for seat in row)

    def _hash(self) -> SeatHash:
        return SeatHash(tuple(tuple(row) for row in self.seats))

    def _neighbors(self, i: int, j: int) -> Generator[str, None, None]:
        for i_delta, j_delta in (
            (-1, 0),
            (+1, 0),
            (0, -1),
            (0, +1),
            (-1, -1),
            (+1, +1),
            (-1, +1),
            (+1, -1),
        ):
            ni, nj = i + i_delta, j + j_delta
            if 0 <= ni < self.height and 0 <= nj < self.width:
                yield self.seats[ni][nj]

    def _visible(self, i: int, j: int) -> Generator[str, None, None]:
        up = range(i - 1, -1, -1), cycle((j,))
        down = range(i + 1, self.height), cycle((j,))
        left = cycle((i,)), range(j - 1, -1, -1)
        right = cycle((i,)), range(j + 1, self.width)

        diag_45 = range(i - 1, -1, -1), range(j + 1, self.width)
        diag_135 = range(i + 1, self.height), range(j + 1, self.width)
        diag_225 = range(i + 1, self.height), range(j - 1, -1, -1)
        diag_315 = range(i - 1, -1, -1), range(j - 1, -1, -1)

        for irange, jrange in (
            up,
            down,
            left,
            right,
            diag_45,
            diag_135,
            diag_225,
            diag_315,
        ):
            seat = self._collect(irange, jrange)
            if seat:
                yield seat

    def _collect(self, irange: Iterable[int], jrange: Iterable[int]) -> str | None:
        return next(
            (
                self.seats[i][j]
                for (i, j) in zip(irange, jrange)
                if self.seats[i][j] != "."
            ),
            None,
        )


def parse(filename: str) -> Ferry:
    with open(filename) as f:
        return Ferry([list(line.strip()) for line in f])


def execute(filename: str, part: int) -> int:
    ferry = parse(filename)
    done = ferry.sit(part)
    while not done:
        done = ferry.sit(part)

    return ferry.count()


def part1(filename: str) -> int:
    return execute(filename, 1)


def part2(filename: str) -> int:
    return execute(filename, 2)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
