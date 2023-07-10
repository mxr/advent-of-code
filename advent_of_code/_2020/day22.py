from __future__ import annotations

from collections import deque


def parse(filename: str) -> tuple[deque[int], deque[int]]:
    with open(filename) as f:
        p1, p2 = f.read().split("\n\n")

    p1d = deque(int(line) for line in p1.splitlines()[1:])
    p2d = deque(int(line) for line in p2.splitlines()[1:])

    return p1d, p2d


def part1(filename: str) -> int:
    p1d, p2d = parse(filename)

    while p1d and p2d:
        p1c, p2c = p1d.popleft(), p2d.popleft()
        if p1c > p2c:
            p1d.extend((p1c, p2c))
        else:
            p2d.extend((p2c, p1c))

    w = p1d or p2d

    return sum(i * n for i, n in enumerate(reversed(w), start=1))


def part2(filename: str) -> int:
    p1d, p2d = parse(filename)

    def recursive_combat(p1d: deque[int], p2d: deque[int]) -> bool:
        seen = set()
        while p1d and p2d:
            h = (tuple(p1d), tuple(p2d))
            if h in seen:
                return True
            seen.add(h)

            p1c, p2c = p1d.popleft(), p2d.popleft()
            if p1c <= len(p1d) and p2c <= len(p2d):
                p1w = recursive_combat(deque(list(p1d)[:p1c]), deque(list(p2d)[:p2c]))
            else:
                p1w = p1c > p2c

            if p1w:
                p1d.extend((p1c, p2c))
            else:
                p2d.extend((p2c, p1c))

        return bool(p1d)

    w = p1d if recursive_combat(p1d, p2d) else p2d

    return sum(i * n for i, n in enumerate(reversed(w), start=1))


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
