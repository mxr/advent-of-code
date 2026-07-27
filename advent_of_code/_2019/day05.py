from __future__ import annotations

import functools
from operator import add
from operator import eq
from operator import lt
from operator import mul

ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
HALT = 99


@functools.cache
def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        return tuple(int(n) for n in f.read().split(","))


def modes_code(code: int) -> tuple[str, int]:
    pm, oc = code // 100, code % 100
    return str(pm).zfill(3), oc


def with_mode(modes: str, codes: list[int], ip: int, offset: int) -> int:
    return codes[ip + offset] if modes[-offset] == "0" else ip + offset


def int_lt(a: int, b: int) -> int:
    return int(lt(a, b))


def int_eq(a: int, b: int) -> int:
    return int(eq(a, b))


THREE_OPS = {ADD: add, MUL: mul, LT: int_lt, EQ: int_eq}
TWO_OPS = {JIT: lambda n: n, JIF: lambda n: not n}
ONE_OP = frozenset((INPUT, OUTPUT))


def run(filename: str, inp: int) -> int:
    codes = list(parse(filename))

    ip = 0
    while codes[ip] != HALT:
        modes, code = modes_code(codes[ip])
        if code in THREE_OPS:
            n1 = codes[with_mode(modes, codes, ip, 1)]
            n2 = codes[with_mode(modes, codes, ip, 2)]
            n3 = codes[ip + 3]

            codes[n3] = THREE_OPS[code](n1, n2)

            ip += 4
            continue

        if code in TWO_OPS:
            n1 = codes[with_mode(modes, codes, ip, 1)]
            n2 = codes[with_mode(modes, codes, ip, 2)]

            ip = n2 if TWO_OPS[code](n1) else ip + 3
            continue

        assert code in ONE_OP, code

        n = with_mode(modes, codes, ip, 1)
        if code == INPUT:
            codes[n] = inp
        else:
            assert code == OUTPUT
            print(codes[n], end=" ")

        ip += 2

    return -1


def part1(filename: str) -> int:
    return run(filename, 1)


def part2(filename: str) -> int:
    return run(filename, 5)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
