from __future__ import annotations

import functools
from operator import add
from operator import mul

ADD = 1
HALT = 99


@functools.cache
def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        return tuple(int(n) for n in f.read().split(","))


def run(filename: str, noun: int, verb: int) -> int:
    ops = list(parse(filename))
    ops[1], ops[2] = noun, verb

    for i in range(0, len(ops), 4):
        op, n1, n2, n3 = ops[i : i + 4]
        if op == HALT:
            break

        ops[n3] = (add if op == ADD else mul)(ops[n1], ops[n2])

    return ops[0]


def part1(filename: str) -> int:
    return run(filename, 12, 2)


def part2(filename: str) -> int:
    for noun in range(100):
        for verb in range(100):
            if run(filename, noun, verb) == 19690720:
                return 100 * noun + verb
    return 0


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
