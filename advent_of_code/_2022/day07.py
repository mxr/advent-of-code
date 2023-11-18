from __future__ import annotations

import bisect
import functools
from dataclasses import dataclass
from dataclasses import field
from typing import Generic
from typing import Protocol
from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class WithName(Protocol):
    name: str


T = TypeVar("T", bound=WithName)


@dataclass
class SetWithAccessor(Generic[T]):
    _items: dict[str, T] = field(default_factory=dict)

    def add(self, node: T) -> None:
        self._items[node.name] = node

    def __getitem__(self, name: str) -> T:
        return self._items[name]

    def __iter__(self) -> Generator[T, None, None]:
        yield from self._items.values()

    def __bool__(self) -> bool:
        return bool(self._items)


@dataclass
class Node:
    name: str
    parent: Node | None = None
    size: int | None = None
    children: SetWithAccessor[Node] = field(default_factory=SetWithAccessor)

    def __hash__(self) -> int:
        return hash(self.name)


def parse(filename: str) -> Node:
    with open(filename) as f:
        next(f)
        curr = Node("/")
        for line in f.readlines():
            if line.startswith("$ ls"):
                continue
            elif line.startswith("dir"):
                d = line.split()[-1]
                curr.children.add(Node(d, curr))
            elif line.startswith("$ cd .."):
                assert curr.parent
                curr = curr.parent
            elif line.startswith("$ cd"):
                d = line.split()[-1]
                curr = curr.children[d]
            else:
                raw_size, name = line.split()
                curr.children.add(Node(name, curr, int(raw_size)))

    root = curr
    while root.parent:
        root = root.parent

    return root


def set_sizes(root: Node) -> int:
    size = sum((set_sizes(c) for c in root.children), root.size or 0)
    root.size = size
    return size


def gen_dir_sizes(root: Node) -> Generator[int, None, None]:
    if not root.children:
        return

    assert root.size
    yield root.size
    for c in root.children:
        yield from gen_dir_sizes(c)


@functools.cache
def dir_sizes(filename: str) -> tuple[int, ...]:
    root = parse(filename)
    _ = set_sizes(root)
    return tuple(gen_dir_sizes(root))


def part1(filename: str) -> int:
    return sum(s for s in dir_sizes(filename) if s < 100000)


def part2(filename: str) -> int:
    ds = sorted(dir_sizes(filename))

    target = 30000000 - (70000000 - ds[-1])
    i = bisect.bisect(ds, target)

    return ds[i]


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
