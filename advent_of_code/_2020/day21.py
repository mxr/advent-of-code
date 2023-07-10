from __future__ import annotations

import functools
import re
from collections import Counter
from collections import defaultdict
from collections.abc import Generator
from typing import NamedTuple
from typing import NewType


RE = re.compile(r"([a-z ]+)\(contains ([^)]+)\)")

Ingredient = NewType("Ingredient", str)
Allergen = NewType("Allergen", str)


class Match(NamedTuple):
    ingredient: Ingredient
    allergen: Allergen


class IngredientList(NamedTuple):
    ingredients: set[Ingredient]
    allergens: set[Allergen]


def parse(
    filename: str,
) -> Generator[IngredientList, None, None]:
    with open(filename) as f:
        for line in f:
            m = RE.match(line)
            assert m, line

            ingredients = {Ingredient(i) for i in m.group(1).split()}
            allergens = {Allergen(s.strip()) for s in m.group(2).split(",")}

            yield IngredientList(ingredients, allergens)


@functools.lru_cache(maxsize=1)
def execute(filename: str) -> tuple[int, str]:
    ing_lists = list(parse(filename))

    ings, algs = set(), set()
    c: Counter[Ingredient] = Counter()
    for il in ing_lists:
        ings.update(il.ingredients)
        algs.update(il.allergens)
        c.update(il.ingredients)

    # part1:
    # if an ingredient is not present in some ingredient list with allergens, that
    # ingredient will never have that allergen
    potential = {Match(i, a) for i in ings for a in algs}
    for il in ing_lists:
        for i in ings - il.ingredients:
            for a in il.allergens:
                potential.discard(Match(i, a))
    potential_ings = {m.ingredient for m in potential}

    p1 = sum(c[i] for i in ings - potential_ings)

    # part 2:
    # collect all possible ingredients for a given allergen. if there's only one
    # ingredient for an allergen, then that ingredient contains that allergen.
    # remove it from our search space and keep repeating until all allergens are
    # accounted for. this is not a general solution - it only works because the
    # problem input lends itself to being able to identify one ingredient at a
    # time. we never end up with ambiguous situations such as
    # `{'foo': {'shellfish', 'eggs'}, 'bar': {'shellfish', 'eggs'}}`
    a2is: dict[Allergen, set[Ingredient]] = defaultdict(set)
    for m in potential:
        a2is[m.allergen].add(m.ingredient)

    dangerous: dict[Ingredient, Allergen] = {}
    while len(dangerous) != len(algs):
        ac = Counter({a: len(iis) for a, iis in a2is.items()})
        for alg, n in ac.items():
            if n == 1:
                i = next(iter(a2is[alg]))

                dangerous[i] = alg
                for iis in a2is.values():
                    iis.discard(i)

            if n == 0:
                del a2is[alg]

    p2 = ",".join(sorted(dangerous, key=lambda i: dangerous[Ingredient(i)]))

    return p1, p2


def part1(filename: str) -> int:
    n, _ = execute(filename)
    return n


def part2(filename: str) -> int:
    _, s = execute(filename)
    print(s)
    return -1


if __name__ == "__main__":
    from advent_of_code.common.main import main

    raise SystemExit(main(part1, part2))
