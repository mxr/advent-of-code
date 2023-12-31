from __future__ import annotations

from typing import NamedTuple


class Fold(NamedTuple):
    dim: str
    val: int


class Paper:
    def __init__(self, marks: list[list[bool]]) -> None:
        self.marks = marks
        self.height, self.width = len(marks), len(marks[0])

    def mark(self, i: int, j: int) -> None:
        self.marks[i][j] = True

    def fold(self, fold: Fold) -> None:
        if fold.dim == "x":
            bf, af = fold.val - 1, fold.val + 1
            while bf >= 0 and af <= self.width:
                for i in range(self.height):
                    self.marks[i][bf] |= self.marks[i][af]
                bf -= 1
                af += 1

            for i in range(self.height):
                self.marks[i] = self.marks[i][: fold.val]

        else:
            bf, af = fold.val - 1, fold.val + 1
            while bf >= 0 and af < self.height:
                for j in range(self.width):
                    self.marks[bf][j] |= self.marks[af][j]
                bf -= 1
                af += 1

            self.marks = self.marks[: fold.val]

        self.height, self.width = len(self.marks), len(self.marks[0])

    def __str__(self) -> str:
        return "\n".join("".join("#" if m else "." for m in row) for row in self.marks)


def parse(filename: str) -> tuple[Paper, list[Fold]]:
    with open(filename) as f:
        coords, raw_folds = f.read().split("\n\n")

    xs, ys = [], []
    for line in coords.splitlines():
        x, _, y = line.partition(",")
        xs.append(int(x))
        ys.append(int(y))

    paper = Paper([[False] * (max(xs) + 1) for _ in range(max(ys) + 1)])
    for j, i in zip(xs, ys, strict=True):
        paper.mark(i, j)

    folds = []
    for line in raw_folds.splitlines():
        raw_dim, _, raw_val = line.partition("=")
        dim, val = raw_dim[-1], int(raw_val)

        folds.append(Fold(dim, val))

    return paper, folds


def part1(filename: str) -> int:
    paper, folds = parse(filename)

    paper.fold(folds[0])

    return sum(m for row in paper.marks for m in row)


def part2(filename: str) -> int:
    paper, folds = parse(filename)

    for fold in folds:
        paper.fold(fold)

    print("\n", paper, sep="")

    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
