from __future__ import annotations

import sys
from argparse import ArgumentParser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def main(part1: Callable[[str], int], part2: Callable[[str], int]) -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument(
        "-f", "--filename", type=str, default=sys.argv[0].replace(".py", ".txt")
    )

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print("part1: ", end="")
        p1 = part1(filename)
        print("" if p1 == -1 else p1)
    if (part or 2) == 2:
        print("part2: ", end="")
        p2 = part2(filename)
        print("" if p2 == -1 else p2)

    return 0
