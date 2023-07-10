from __future__ import annotations

from collections.abc import Generator
from operator import add
from operator import mul


class Expr:
    def __init__(self, inp: str) -> None:
        self.inp = inp

    def evaluate(self, precedence: dict[str, int]) -> int:
        """adapted from https://archive.ph/FAJ9I"""
        postfix: list[int | str] = []
        ops: list[str] = []

        i = 0
        while i < len(self.inp):
            c = self.inp[i]
            if c == "*" or c == "+":
                while ops and precedence[c] <= precedence[ops[-1]]:
                    postfix.append(ops.pop())
                ops.append(c)
            elif "0" <= c <= "9":
                postfix.append(int(c))
            elif c == "(":
                bc = 0
                j = i
                while j < len(self.inp):
                    jc = self.inp[j]
                    if jc == "(":
                        bc += 1
                    elif jc == ")":
                        bc -= 1
                        if bc == 0:
                            break
                    j += 1

                postfix.append(Expr(self.inp[i + 1 : j]).evaluate(precedence))
                i = j

            i += 1

        postfix.extend(reversed(ops))

        s = []
        for p in postfix:
            if isinstance(p, int):
                s.append(p)
            else:
                s.append((mul if p == "*" else add)(s.pop(), s.pop()))

        return s[0]


def parse(filename: str) -> Generator[Expr, None, None]:
    with open(filename) as f:
        for line in f:
            yield Expr(line.strip())


def execute(filename: str, precedence: dict[str, int]) -> int:
    return sum(expr.evaluate(precedence) for expr in parse(filename))


def part1(filename: str) -> int:
    return execute(filename, {"+": 1, "*": 1})


def part2(filename: str) -> int:
    return execute(filename, {"+": 2, "*": 1})


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
