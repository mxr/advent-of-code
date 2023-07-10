from __future__ import annotations

from collections.abc import Generator
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import chain


@dataclass
class Node:
    n: int
    nn: Node | None = None

    @staticmethod
    def from_nums(nums: Iterable[int]) -> Node:
        f, *r = nums
        h = Node(f)

        c = h
        for n in r:
            c.nn = Node(n)
            c = c.nn

        return h

    def next(self) -> Node:  # noqa: A003
        # should only be called when we know this isn't null
        return self.nn  # type: ignore

    def by_nums(self) -> dict[int, Node]:
        d = {}
        c: Node | None = self
        while c is not None:
            d[c.n] = c
            c = c.nn
        return d

    def tail(self) -> Node:
        c = self
        while c.nn is not None:
            c = c.nn
        return c

    def size(self) -> int:
        size = 0
        c: Node | None = self
        while c is not None:
            c = c.nn
            size += 1

        return size

    def __repr__(self) -> str:
        ns = []
        c: Node | None = self
        while c is not None:
            ns.append(c.n)
            c = c.nn

        return f"Node({ns!r})"


def parse(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        for c in f.read().strip():
            yield int(c)


def execute(cups: Node, moves: int) -> Node:
    size = cups.size()
    tail = cups.tail()
    by_nums = cups.by_nums()

    for _ in range(moves):
        h = cups

        p = []
        ps = h.next()
        curr = ps
        for _ in range(3):
            pe = curr
            p.append(curr.n)
            curr = curr.next()

        d = (h.n - 2) % size + 1
        while d in p:
            d = (d - 2) % size + 1

        h.nn = pe.next()
        curr = by_nums[d]
        dn = curr.nn
        curr.nn = ps
        pe.nn = dn

        # TODO avoid searching for the tail
        while tail.nn is not None:
            tail = tail.nn
        tail.nn = h
        cups = h.nn
        h.nn = None
        tail = h

    return cups


def part1(filename: str) -> int:
    cups = Node.from_nums(parse(filename))

    moved = execute(cups, 100)

    nums = []
    c: Node | None = moved
    while c is not None:
        nums.append(c.n)
        c = c.nn

    i = nums.index(1)

    return int("".join(str(c) for c in chain(nums[i + 1 :], nums[:i])))


def part2(filename: str) -> int:
    nums = list(parse(filename))
    cups = Node.from_nums(chain(nums, range(max(nums) + 1, 1_000_000 + 1)))

    moved = execute(cups, 10_000_000)

    c = moved
    while True:
        if c.n == 1:
            break
        c = c.next()

    cn1 = c.next()
    cn2 = cn1.next()

    return cn1.n * cn2.n


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
