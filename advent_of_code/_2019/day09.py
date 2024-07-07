from __future__ import annotations

import functools
from collections import defaultdict
from operator import add
from operator import eq
from operator import lt
from operator import mul
from typing import TypeVar


T = TypeVar("T")

ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
REL = 9
HALT = 99


@functools.cache
def parse(filename: str) -> tuple[int, ...]:
    with open(filename) as f:
        return tuple(int(n) for n in f.read().split(","))


def modes_code(code: int) -> tuple[str, int]:
    pm, oc = code // 100, code % 100
    return str(pm).zfill(3), oc


def with_mode(modes: str, codes: dict[int, int], ip: int, rel: int, offset: int) -> int:
    m = modes[-offset]
    if m == "0":
        return codes[ip + offset]
    elif m == "1":
        return ip + offset
    else:
        assert m == "2"
        return codes[ip + offset] + rel


def int_lt(a: int, b: int) -> int:
    return int(lt(a, b))


def int_eq(a: int, b: int) -> int:
    return int(eq(a, b))


THREE_OPS = {ADD: add, MUL: mul, LT: int_lt, EQ: int_eq}
TWO_OPS = {JIT: lambda n: n, JIF: lambda n: not n}
ONE_OP = frozenset((INPUT, OUTPUT, REL))


def run(codes: dict[int, int], inp: int) -> list[int]:
    ip = 0
    rel = 0
    out = []

    while codes[ip] != HALT:
        modes, code = modes_code(codes[ip])
        if code in THREE_OPS:
            n1 = codes[with_mode(modes, codes, ip, rel, 1)]
            n2 = codes[with_mode(modes, codes, ip, rel, 2)]
            n3 = with_mode(modes, codes, ip, rel, 3)

            codes[n3] = THREE_OPS[code](n1, n2)

            ip += 4
            continue

        if code in TWO_OPS:
            n1 = codes[with_mode(modes, codes, ip, rel, 1)]
            n2 = codes[with_mode(modes, codes, ip, rel, 2)]

            ip = n2 if TWO_OPS[code](n1) else ip + 3
            continue

        assert code in ONE_OP, code

        n = with_mode(modes, codes, ip, rel, 1)
        if code == INPUT:
            codes[n] = inp
        elif code == OUTPUT:
            out.append(codes[n])
        else:
            assert code == REL
            rel += codes[n]

        ip += 2

    return out


def solve(filename: str, inp: int) -> None:
    print(run(defaultdict(int, enumerate(parse(filename))), inp))


def part1(filename: str) -> int:
    solve(filename, 1)
    return -1


def part2(filename: str) -> int:
    solve(filename, 2)
    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
