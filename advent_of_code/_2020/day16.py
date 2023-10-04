from __future__ import annotations

import re
from collections import defaultdict
from typing import NamedTuple
from typing import NewType

RE = re.compile(r"(\d+)-(\d+)")


class Range(NamedTuple):
    min: int  # noqa: A003
    max: int  # noqa: A003

    def valid(self, n: int) -> bool:
        return self.min <= n <= self.max


class Rule(NamedTuple):
    name: str
    ranges: list[Range]

    def valid(self, n: int) -> bool:
        return any(r.valid(n) for r in self.ranges)


Ticket = NewType("Ticket", list[int])


def parse(filename: str) -> tuple[list[Rule], Ticket, list[Ticket]]:
    with open(filename) as f:
        raw_rules, raw_yours, raw_nearby = f.read().split("\n\n")

    rules = []
    for r in raw_rules.split("\n"):
        raw_name, _, raw_ranges = r.partition(":")
        ranges = [Range(int(mn), int(mx)) for mn, mx in RE.findall(raw_ranges)]

        rules.append(Rule(raw_name.strip(), ranges))

    yours = Ticket([int(t) for t in raw_yours.splitlines()[-1].split(",")])

    nearby = [
        Ticket([int(t) for t in ticket.split(",")])
        for ticket in raw_nearby.splitlines()[1:]
    ]

    return rules, yours, nearby


def part1(filename: str) -> int:
    rules, _, nearby = parse(filename)

    return sum(
        t
        for ticket in nearby
        for t in ticket
        if not any(rule.valid(t) for rule in rules)
    )


def part2(filename: str) -> int:
    rules, yours, nearby = parse(filename)

    valid_tickets = [ticket for ticket in nearby if valid(ticket, rules)]

    names = defaultdict(set)
    for i in range(len(yours)):
        for rule in rules:
            if all(rule.valid(ticket[i]) for ticket in valid_tickets):
                names[rule.name].add(i)

    out = {}
    while names:
        positions_to_pop = []
        names_to_pop = []
        for name, positions in names.items():
            if len(positions) == 1:
                p = positions.pop()
                positions_to_pop.append(p)
                names_to_pop.append(name)
                out[name] = p

        for positions in names.values():
            if p in positions:
                positions.remove(p)

        for name in names_to_pop:
            del names[name]

    product = 1
    for name, position in out.items():
        if name.startswith("departure"):
            product *= yours[position]

    return product


def valid(ticket: Ticket, rules: list[Rule]) -> bool:
    return any(all(rule.valid(t) for t in ticket) for rule in rules)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
