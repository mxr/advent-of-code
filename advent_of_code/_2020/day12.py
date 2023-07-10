from __future__ import annotations

from collections.abc import Generator


DIRS = ["N", "E", "S", "W"]


class Ship:
    def __init__(self) -> None:
        self.direction = "E"
        self.x, self.y = 0, 0

    def move(self, direction: str, dist: int) -> None:
        if direction == "N":
            self.y -= dist
        elif direction == "S":
            self.y += dist
        elif direction == "W":
            self.x -= dist
        elif direction == "E":
            self.x += dist
        elif direction == "F":
            self.move(self.direction, dist)
        else:
            steps = (-1) ** (direction == "L") * dist // 90
            dir_index = DIRS.index(self.direction)
            new_index = (dir_index + steps) % len(DIRS)
            self.direction = DIRS[new_index]

    def dist(self) -> int:
        return abs(self.x) + abs(self.y)


class ShipWithWaypoint:
    def __init__(self) -> None:
        self.direction = "E"
        self.x, self.y = 0, 0
        self.wx, self.wy = 10, -1  # relative coords

    def move(self, direction: str, dist: int) -> None:
        if direction == "N":
            self.wy -= dist
        elif direction == "S":
            self.wy += dist
        elif direction == "W":
            self.wx -= dist
        elif direction == "E":
            self.wx += dist
        elif direction == "F":
            self.x += self.wx * dist
            self.y += self.wy * dist
        else:
            steps = ((-1) ** (direction == "L") * dist // 90) % len(DIRS)
            if steps in (1, -3):
                self.wx, self.wy = -self.wy, self.wx
            elif steps in (2, -2):
                self.wx, self.wy = -self.wx, -self.wy
            elif steps in (3, -1):
                self.wx, self.wy = self.wy, -self.wx
            else:
                # no movement
                pass

    def dist(self) -> int:
        return abs(self.x) + abs(self.y)


def parse(filename: str) -> Generator[tuple[str, int], None, None]:
    with open(filename) as f:
        for line in f:
            yield line[0], int(line[1:])


def part1(filename: str) -> int:
    s = Ship()
    for direction, dist in parse(filename):
        s.move(direction, dist)

    return s.dist()


def part2(filename: str) -> int:
    s = ShipWithWaypoint()
    for direction, dist in parse(filename):
        s.move(direction, dist)

    return s.dist()


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
