from __future__ import annotations

import functools
from itertools import cycle
from itertools import permutations
from operator import add
from operator import eq
from operator import lt
from operator import mul
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

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


# generator IO technique adapted from anthonywritescode
def run(codes: list[int], inp: int) -> Generator[int | None, int]:
    ip = 0

    read_inp = False
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
            if not read_inp:
                codes[n] = inp
                read_inp = True
            else:
                codes[n] = yield None
        else:
            assert code == OUTPUT
            yield codes[n]

        ip += 2

    return


def must[T](t: T | None) -> T:
    assert t is not None
    return t


def part1(filename: str) -> int:
    codes = parse(filename)
    m = 0

    for ps in permutations(range(5)):
        prev = 0
        for p in ps:
            amp = run(list(codes), p)
            next(amp)
            prev = must(amp.send(prev))
        m = max(m, prev)

    return m


def part2(filename: str) -> int:
    codes = parse(filename)
    m = 0

    for ps in permutations(range(5, 10)):
        amps = cycle([run(list(codes), p) for p in ps])
        prev = 0
        try:
            while True:
                amp = next(amps)
                next(amp)
                prev = must(amp.send(prev))
        except StopIteration:
            pass

        m = max(m, prev)

    return m


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
