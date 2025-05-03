# pyright: reportExplicitAny=false

import random

from typing import Any, Callable, Self
from urllib.parse import urlencode
from collections import OrderedDict
from collections.abc import Generator


def url_build(root: str, **param: object) -> str:
    return f"{root}?{urlencode(OrderedDict(**param))}"


def random_order[T](items: list[T], inplace: bool = False) -> Generator[T, None, None]:
    array: list[T] = items if inplace else list(items)

    n = len(array)
    for i in range(n - 1, -1, -1):
        j = random.randrange(i + 1)
        yield array[j]
        array[j], array[i] = array[i], array[j]


class Defer:
    def __init__(self):
        self.funs: list[Callable[[], Any]] = []

    def __call__(self, fun: Callable[[], Any]) -> None:
        self.funs.append(fun)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        for fun in reversed(self.funs):
            try:
                fun()
            except Exception:
                pass


def close_enough(x: float, target: float, delta: float = 0.001) -> bool:
    return abs(target - x) <= delta
