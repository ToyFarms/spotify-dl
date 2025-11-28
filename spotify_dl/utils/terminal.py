# pyright: reportUnknownMemberType=false, reportMissingTypeStubs=false, reportAny=false, reportExplicitAny=false
import wcwidth

from collections.abc import Iterable, Iterator
from collections import defaultdict
from typing import Any, Callable, cast
from collections.abc import Sequence, Mapping, ItemsView


def realwidth(s: str) -> int:
    return wcwidth.wcswidth(s) or 0


def to_text(obj: Any) -> str:
    if isinstance(obj, str):
        return obj
    return repr(obj)


def get_max_width(texts: Iterable[str]) -> int:
    return max((realwidth(t) for t in texts), default=0)


def sort_by_types[T, K](
    iter: Iterable[T],
    order: list[type[object]],
    key: Callable[[T], T | K] = lambda x: x,
) -> Iterator[T]:
    buckets: defaultdict[type[T | K], list[T]] = defaultdict(list)
    other_types: list[type[T | K]] = list()
    for x in iter:
        x_type = type(key(x))
        buckets[x_type].append(x)
        if x_type not in order and x_type not in other_types:
            other_types.append(x_type)

    for t in order:
        for x in buckets.get(cast(type[T], t), []):
            yield x

    for t in other_types:
        for x in buckets.get(t, []):
            yield x


def print_table(
    data: Any,
    indent: int = 4,
    _depth: int = 0,
) -> None:
    prefix = " " * (indent * _depth)

    if isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
        for index, element in enumerate(data):
            print_table(element, indent, _depth)
            if index < len(data) - 1:
                print(f"{prefix}{'-' * 4}")
        return

    if isinstance(data, Mapping):
        primitive_keys = [
            to_text(k)
            for k, v in cast(ItemsView[Any, object], data.items())
            if not isinstance(v, (Mapping, Sequence))
            or isinstance(v, (str, bytes, bytearray))
        ]
        key_width = get_max_width(primitive_keys)

        def kind(v: Any) -> int:
            if isinstance(v, Mapping):
                return 2
            if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):
                return 1
            return 0

        sorted_items = sorted(
            cast(ItemsView[Any, object], data.items()), key=lambda kv: kind(kv[1])
        )

        for key, value in sorted_items:
            ktext = to_text(key)
            if isinstance(value, Mapping):
                print(f"{prefix}{ktext}:")
                print_table(value, indent, _depth + 1)
            elif isinstance(value, Sequence) and not isinstance(
                value, (str, bytes, bytearray)
            ):
                print(f"{prefix}{ktext} [")
                print_table(value, indent, _depth + 1)
                print(f"{prefix}]")
            else:
                vtext = to_text(value)
                print(f"{prefix}{ktext.ljust(key_width)} : {vtext}")
        return

    print(f"{prefix}{to_text(data)}")
