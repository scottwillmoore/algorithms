from __future__ import annotations
from typing import Callable, Collection, Protocol, TypeVar


_Element = TypeVar("_Element")


_Comparator = Callable[[_Element, _Element], bool]


class PriorityQueue(Collection[_Element], Protocol[_Element]):
    """
    # Priority queue

    An abstract data structure (ADT) whereby each element has an associated
    priority. The element with the highest priority is retrieved before an
    element with a lower priority.

    https://en.wikipedia.org/wiki/Priority_queue
    """

    def peek(self) -> _Element:
        pass

    def pop(self) -> _Element:
        pass

    def push(self, element: _Element) -> None:
        pass
