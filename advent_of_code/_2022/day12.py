from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import dijkstar  # pip install Dijkstar

if TYPE_CHECKING:
    from collections.abc import Generator


def neighbors(i: int, j: int) -> Generator[tuple[int, int]]:
    yield i - 1, j
    yield i, j - 1
    yield i + 1, j
    yield i, j + 1


def val(c: str) -> int:
    if c == "S":
        return val("a")
    elif c == "E":
        return val("z")
    else:
        return ord(c)


def parse(
    filename: str,
) -> tuple[dijkstar.Graph, list[tuple[int, int]], tuple[int, int]]:
    graph = dijkstar.Graph()

    start = (-1, -1)
    starts = []
    end = (-1, -1)

    with open(filename) as f:
        grid = tuple(tuple(line.strip()) for line in f)

    width, height = len(grid[0]), len(grid)
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
            elif c == "a":
                starts.append((i, j))

            for ni, nj in neighbors(i, j):
                if 0 <= ni < height and 0 <= nj < width:
                    vn, v = val(grid[ni][nj]), val(c)
                    if vn - v <= 1:
                        graph.add_edge((i, j), (ni, nj), 1)
                    if v - vn <= 1:
                        graph.add_edge((ni, nj), (i, j), 1)

    starts.append(start)

    return graph, starts, end


def part1(filename: str) -> int:
    graph, starts, end = parse(filename)
    path = dijkstar.find_path(graph, starts[-1], end)
    return path.total_cost


def part2(filename: str) -> int:
    graph, starts, end = parse(filename)

    m = float("inf")
    for s in starts:
        with contextlib.suppress(dijkstar.NoPathError):
            dijkstar.single_source_shortest_paths()
            tc = dijkstar.find_path(graph, s, end).total_cost
            m = min(m, tc)

    return int(m)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
