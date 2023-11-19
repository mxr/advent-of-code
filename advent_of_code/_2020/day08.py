from __future__ import annotations

import itertools
from typing import NamedTuple
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class Instruction(NamedTuple):
    cmd: str
    val: int


def parse(filename: str) -> Generator[Instruction, None, None]:
    with open(filename) as f:
        for line in f:
            name, _, val = line.partition(" ")
            yield Instruction(name, int(val))


def part1(filename: str) -> int:
    instructions = list(parse(filename))
    return execute(instructions)[1]


def execute(instructions: list[Instruction]) -> tuple[bool, int]:
    seen = set()
    ip, acc = 0, 0
    while ip < len(instructions):
        if ip in seen:
            return True, acc
        seen.add(ip)

        instr = instructions[ip]
        if instr.cmd == "acc":
            acc += instr.val
            ip += 1
        elif instr.cmd == "jmp":
            ip += instr.val
        else:
            ip += 1

    return False, acc


def part2(filename: str) -> int:
    instructions = list(parse(filename))
    for i, instr in enumerate(instructions):
        if instr.cmd == "nop":
            new_cmd = "jmp"
        elif instr.cmd == "jmp":
            new_cmd = "nop"
        else:
            continue

        new_instructions = list(
            itertools.chain(
                instructions[:i],
                (Instruction(new_cmd, instr.val),),
                instructions[i + 1 :],
            )
        )
        dup, acc = execute(new_instructions)
        if not dup:
            return acc

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
