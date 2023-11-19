from __future__ import annotations

import re
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


RE = re.compile(r"mem\[(\d+)\] = (\d+)")


class Command(NamedTuple):
    address: int
    value: int


class MaskCommands(NamedTuple):
    mask: str
    mask0: int
    mask1: int
    commands: list[Command]


def parse(filename: str) -> Generator[MaskCommands, None, None]:
    with open(filename) as f:
        chunks = iter(f.read().strip().split("mask"))
        next(chunks)  # blank line

        for chunk in chunks:
            raw_mask, raw_mems = chunk.split("\n", 1)

            _, _, mask = raw_mask.partition(" = ")
            mask0 = int(mask.translate({ord("X"): "0"}), 2)
            mask1 = int(mask.translate({ord("X"): "1"}), 2)

            commands = [Command(int(a), int(v)) for a, v in RE.findall(raw_mems)]

            yield MaskCommands(mask, mask0, mask1, commands)


def part1(filename: str) -> int:
    memory = {}
    for mc in parse(filename):
        for c in mc.commands:
            memory[c.address] = mc.mask0 | c.value & mc.mask1

    return sum(memory.values())


def part2(filename: str) -> int:
    memory = {}
    for mc in parse(filename):
        for c in mc.commands:
            for addr in gen_addrs(apply(mc.mask, c.address)):
                memory[addr] = c.value

    return sum(memory.values())


def apply(mask: str, address: int) -> str:
    return "".join(
        a if m == "0" else "1" if m == "1" else "X"
        for (m, a) in zip(mask, format(address, "036b"), strict=True)
    )


def gen_addrs(mask: str) -> Generator[int, None, None]:
    if "X" in mask:
        yield from gen_addrs(mask.replace("X", "0", 1))
        yield from gen_addrs(mask.replace("X", "1", 1))
    else:
        yield int(mask, 2)


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
