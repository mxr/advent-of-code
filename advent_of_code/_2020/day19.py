from __future__ import annotations

import functools
import re


def parse(filename: str) -> tuple[dict[int, str], list[str]]:
    with open(filename) as f:
        s1, s2 = f.read().split("\n\n")

    rules = {}
    for rule in s1.splitlines():
        n, _, r = rule.partition(":")
        rules[int(n)] = r.strip()

    return rules, s2.splitlines()


def part1(filename: str) -> int:
    rules, msgs = parse(filename)

    @functools.lru_cache(len(rules))
    def expand(s: str) -> str:
        if "|" in s:
            left, _, right = s.partition("|")
            return f"(({expand(left)})|({expand(right)}))"

        ps = s.split()
        if ps == ['"a"'] or ps == ['"b"']:
            return ps[0][1]

        return "".join(expand(rules[int(p)]) for p in ps)

    regex = re.compile(f"^{expand(rules[0])}$")

    return sum(bool(regex.match(m)) for m in msgs)


def part2(filename: str) -> int:
    rules, msgs = parse(filename)

    rules.update({8: "42 | 42 8", 11: "42 31 | 42 11 31"})

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
