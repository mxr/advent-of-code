from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def parse(filename: str) -> Generator[str]:
    with open(filename) as f:
        for line in f:
            yield line.strip()


def part1(filename: str) -> int:
    first = next(parse(filename))
    gamma_counter = [int(c == "1") for c in first]
    for word in parse(filename):
        for i, c in enumerate(word):
            gamma_counter[i] += 1 if c == "1" else -1

    gamma_str = "".join("1" if b > 0 else "0" for b in gamma_counter)
    gamma = int(gamma_str, 2)

    epsilon = ~gamma & int("1" * len(first), 2)

    return gamma * epsilon


def part2(filename: str) -> int:
    words = list(parse(filename))

    mc = find_most_common(words)
    lc = find_least_common(words)

    return int(mc, 2) * int(lc, 2)


FIND_MOST = "MOST"
FIND_LEAST = "LEAST"


def find_most_common(words: list[str]) -> str:
    return _find(words, FIND_MOST)


def find_least_common(words: list[str]) -> str:
    return _find(words, FIND_LEAST)


def _find(words: list[str], which: str) -> str:
    assert words

    def helper(
        words: list[str],
        which: str,
        pos: int,
    ) -> list[str]:
        if len(words) == 1:
            return words

        tar = target(words, which, pos)
        new_words = [word for word in words if word[pos] == tar]

        return helper(new_words, which, pos + 1)

    def target(words: list[str], which: str, pos: int) -> str:
        counts = Counter(word[pos] for word in words)
        (most, most_val), (least, least_val) = counts.most_common()

        if most_val == least_val:
            return "1" if which == FIND_MOST else "0"

        return most if which == FIND_MOST else least

    return helper(words, which, 0)[0]


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
