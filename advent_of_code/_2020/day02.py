from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

RE = re.compile(r"(\d+)-(\d+)\s+(\w+):\s+(\w+)")


@dataclass
class Validator:
    left: int
    right: int
    char: str

    def valid_part1(self, password: str) -> bool:
        return self.left <= password.count(self.char) <= self.right

    def valid_part2(self, password: str) -> bool:
        # fmt: off
        return (
            (password[self.left - 1] == self.char) !=
            (password[self.right - 1] == self.char)
        )
        # fmt: on


def parse(filename: str) -> Generator[tuple[Validator, str]]:
    with open(filename) as f:
        for left, right, char, pw in RE.findall(f.read()):
            yield Validator(int(left), int(right), char), pw


def part1(filename: str) -> int:
    return sum(v.valid_part1(pw) for v, pw in parse(filename))


def part2(filename: str) -> int:
    return sum(v.valid_part2(pw) for v, pw in parse(filename))


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
