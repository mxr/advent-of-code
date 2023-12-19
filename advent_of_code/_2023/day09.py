from __future__ import annotations

import functools
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@functools.cache
def parse(filename: str) -> tuple[tuple[int, ...], ...]:
    def gen() -> Generator[tuple[int, ...], None, None]:
        with open(filename) as f:
            for line in f:
                yield tuple(int(n) for n in line.split())

    return tuple(gen())


def part1(filename: str) -> int:
    t = 0
    for seq in parse(filename):
        seqs = [list(seq)]
        while not all(n == 0 for n in seqs[-1]):
            curr = seqs[-1]

            new_seq = []
            for i in range(1, len(curr)):
                new_seq.append(curr[i] - curr[i - 1])

            seqs.append(new_seq)

        for i in range(len(seqs) - 2, -1, -1):
            seqs[i].append(seqs[i][-1] + seqs[i + 1][-1])
        
        t += seqs[0][-1]

    return t


def part2(filename: str) -> int:
    t = 0
    for seq in parse(filename):
        seqs = [deque(seq)]
        while not all(n == 0 for n in seqs[-1]):
            curr = seqs[-1]

            new_seq: deque[int] = deque()
            for i in range(1, len(curr)):
                new_seq.append(curr[i] - curr[i - 1])

            seqs.append(new_seq)

        for i in range(len(seqs) - 2, -1, -1):
            seqs[i].appendleft(seqs[i][0] - seqs[i + 1][0])
        
        t += seqs[0][0]

    return t


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
