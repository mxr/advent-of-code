from __future__ import annotations

import functools
from collections import defaultdict


@functools.cache
def parse(filename: str) -> tuple[tuple[str, str], ...]:
    def p(line: str) -> tuple[str, str]:
        s, _, e = line.partition(")")
        return s, e.rstrip()

    with open(filename) as f:
        return tuple(sorted(p(line) for line in f))


def part1(filename: str) -> int:
    pairs = parse(filename)
    graph = defaultdict(list)
    for s, e in pairs:
        graph[s].append(e)

    orbits = 0
    depth = 0
    q = ["COM"]
    while q:
        depth += 1
        q = [e for s in q for e in graph[s]]
        orbits += depth * len(q)

    return orbits


def part2(filename: str) -> int:
    pairs = parse(filename)
    graph = defaultdict(list)
    for s, e in pairs:
        graph[s].append(e)
        graph[e].append(s)

    vertices = set(graph)
    dists = {v: float("inf") for v in vertices} | {"YOU": 0}

    q = set(vertices)
    while q:
        u = min(q, key=lambda v: dists[v])
        if u == "SAN":
            # return number of hops which is 2 less than path length
            return int(dists[u]) - 2

        q.remove(u)
        for v in graph[u]:
            dists[v] = min(dists[u] + 1, dists[v])

    raise AssertionError("unreachable")


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
