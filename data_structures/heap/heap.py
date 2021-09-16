from __future__ import annotations
from collections.abc import Collection
from typing import Callable, Protocol, TypeVar


Element = TypeVar("Element")


Comparator = Callable[[Element, Element], bool]


MIN_COMPARATOR: Comparator = lambda x, y: x < y
MAX_COMPARATOR: Comparator = lambda x, y: x < y


class Node(Protocol[Element]):
    element: Element


# FEATURE: At the moment you cannot define associated types in a Protocol...
# https://github.com/python/typing/issues/548
# https://github.com/python/mypy/issues/7790
class Heap(Collection[Element], Protocol[Element]):
    comparator: Comparator[Element]

    def decrease_node(self, node: Node[Element]) -> None:
        pass

    def delete_node(self, node: Node[Element]) -> None:
        pass

    def merge(self, heap: Heap[Element]) -> None:
        pass

    def peek_node(self) -> Node[Element]:
        pass

    def pop_node(self) -> Node[Element]:
        pass

    def push_node(self, node: Node[Element]) -> None:
        pass
