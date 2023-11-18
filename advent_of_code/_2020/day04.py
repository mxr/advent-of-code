from __future__ import annotations

import itertools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

RE_PAIR = re.compile(r"(\w+):([#:\w]+)")

RE_YEAR = re.compile(r"^\d{4}$")
RE_HEIGHT = re.compile(r"^(\d{2,3})(in|cm)$")
RE_HAIR = re.compile(r"^#[0-9a-f]{6}$")
RE_EYE = re.compile("^(amb|blu|brn|gry|grn|hzl|oth)$")
RE_PASSPORT = re.compile(r"^\d{9}$")

KEYS = frozenset(
    (
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        "cid",
    )
)

OPTIONAL_KEYS = frozenset(("cid",))


def parse(filename: str) -> Generator[dict[str, str], None, None]:
    with open(filename) as f:
        chunk = []
        # the ('', ) ensures the last chunk gets yielded
        for line in itertools.chain(f.read().splitlines(), ("",)):
            if line:
                chunk.append(line)
            else:
                yield {k: v for c in chunk for k, v in RE_PAIR.findall(c)}
                chunk = []


def part1(filename: str) -> int:
    return sum(validate_part1(chunk) for chunk in parse(filename))


def validate_part1(chunk: dict[str, str]) -> bool:
    return KEYS.difference(chunk) <= OPTIONAL_KEYS


def part2(filename: str) -> int:
    return sum(validate_part2(chunk) for chunk in parse(filename))


def validate_part2(chunk: dict[str, str]) -> bool:
    return (
        validate_part1(chunk)
        and validate_year(chunk["byr"], 1920, 2002)
        and validate_year(chunk["iyr"], 2010, 2020)
        and validate_year(chunk["eyr"], 2020, 2030)
        and validate_height(chunk["hgt"])
        and validate_hair(chunk["hcl"])
        and validate_eye(chunk["ecl"])
        and validate_passport(chunk["pid"])
    )


def validate_year(val: str, start: int, end: int) -> bool:
    match = RE_YEAR.match(val)
    if not match:
        return False

    n = int(match.group(0))
    return start <= n <= end


def validate_height(val: str) -> bool:
    match = RE_HEIGHT.match(val)
    if not match:
        return False

    height, unit = int(match.group(1)), match.group(2)
    # fmt: off
    return (
        (unit == "cm" and 150 <= height <= 193) or
        (unit == "in" and 59 <= height <= 76)
    )
    # fmt: on


def validate_hair(val: str) -> bool:
    return bool(RE_HAIR.match(val))


def validate_eye(val: str) -> bool:
    return bool(RE_EYE.match(val))


def validate_passport(val: str) -> bool:
    return bool(RE_PASSPORT.match(val))


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
