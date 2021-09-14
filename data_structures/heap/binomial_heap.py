from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar


T = TypeVar("T")
Comparator = Callable[[T, T], bool]


MIN_COMPARATOR: Comparator = lambda x, y: x < y
MAX_COMPARATOR: Comparator = lambda x, y: x > y


@dataclass
class BinomialNode(Generic[T]):
    element: T
    degree: int = 0
    parent: Optional[BinomialNode[T]] = None
    right_sibling: Optional[BinomialNode[T]] = None
    left_child: Optional[BinomialNode[T]] = None


def combine(
    head_a: Optional[BinomialNode[T]], head_b: Optional[BinomialNode[T]]
) -> Optional[BinomialNode[T]]:
    if not head_a:
        return head_b

    if not head_b:
        return head_a

    if head_a.degree < head_b.degree:
        head = head_a
        head_a = head_a.right_sibling
    else:
        head = head_b
        head_b = head_b.right_sibling

    current = head

    while head_a and head_b:
        if head_a.degree < head_b.degree:
            current.right_sibling = head_a
            current = current.right_sibling
            head_a = head_a.right_sibling

        else:
            current.right_sibling = head_b
            current = current.right_sibling
            head_b = head_b.right_sibling

    if head_a:
        current.right_sibling = head_a
    else:
        current.right_sibling = head_b

    return head


def consolidate(
    head: Optional[BinomialNode[T]], *, comparator: Comparator
) -> Optional[BinomialNode[T]]:
    if not head:
        return head

    previous = None
    current = head
    next = current.right_sibling

    while next:
        is_current_equal = current.degree == next.degree
        is_next_equal = next.right_sibling and next.degree == next.right_sibling.degree

        move_forward = not is_current_equal or is_next_equal

        if move_forward:
            previous = current
            current = next
        else:
            if comparator(current.element, next.element):
                current.right_sibling = next.right_sibling

                link(current, next)

            else:
                if not previous:
                    head = next
                else:
                    previous.right_sibling = next

                link(next, current)

                current = next

        next = current.right_sibling

    return head


def extract(
    head: Optional[BinomialNode[T]], *, comparator: Comparator
) -> tuple[Optional[BinomialNode[T]], Optional[BinomialNode[T]]]:
    if not head:
        return None, None

    previous = None
    current = head

    match_previous = previous
    match = current

    while current:
        if comparator(current.element, match.element):
            match_previous = previous
            match = current

        previous = current
        current = current.right_sibling

    if not match_previous:
        head = match.right_sibling
    else:
        match_previous.right_sibling = match.right_sibling

    remainder = reverse(match.left_child)

    return match, merge(head, remainder, comparator=comparator)


def link(
    head_a: Optional[BinomialNode[T]], head_b: Optional[BinomialNode[T]]
) -> Optional[BinomialNode[T]]:
    head_b.parent = head_a
    head_b.right_sibling = head_a.left_child

    head_a.degree += 1
    head_a.left_child = head_b


def merge(
    head_a: Optional[BinomialNode[T]],
    head_b: Optional[BinomialNode[T]],
    *,
    comparator: Comparator,
) -> Optional[BinomialNode[T]]:
    return consolidate(combine(head_a, head_b), comparator=comparator)


def reverse(head: Optional[BinomialNode[T]]) -> Optional[BinomialNode[T]]:
    previous = None
    current = head

    while current:
        next = current.right_sibling

        current.right_sibling = previous

        previous = current
        current = next

    return previous


def show(node: Optional[BinomialNode[T]], depth=0):
    if not node:
        return

    indent = depth * ".   "
    print(f"{indent}{node.element} ({node.degree})")
    show(node.left_child, depth=depth + 1)
    show(node.right_sibling, depth=depth)


class BinomialHeap(Generic[T]):
    def __init__(
        self,
        head: Optional[BinomialNode[T]] = None,
        *,
        comparator: Comparator = MIN_COMPARATOR,
    ):
        self.head = head
        self.comparator = comparator

    def extract(self) -> Optional[T]:
        match, self.head = extract(self.head, comparator=self.comparator)
        if match:
            return match.element
        else:
            return None

    def insert(self, element: T):
        remainder = BinomialNode(element)
        self.head = merge(self.head, remainder, comparator=self.comparator)

    def merge(self, other: BinomialHeap[T]):
        self.head = merge(self.head, other.head, comparator=self.comparator)
        other.head = None


if __name__ == "__main__":
    heap = BinomialHeap()
    heap.insert(1)
    for i in range(2, 10):
        heap.insert(i)

    for i in range(1, 10):

        print("~~~")
        j = heap.extract()
        print(i, j)
        print("~~~")

        assert i == j

    # h1 = BinomialHeap(12)
    # h1.sibling = BinomialHeap(7)
    # h1.sibling.degree = 1
    # h1.sibling.sibling = BinomialHeap(15)
    # h1.sibling.sibling.degree = 2

    # h2 = BinomialHeap(18)
    # h2.sibling = BinomialHeap(3)
    # h2.sibling.degree = 1
    # h2.sibling.sibling = BinomialHeap(6)
    # h2.sibling.sibling.degree = 4

    # node = h1.merge(h2)
    # # node = h2.merge2(h1)
    # while node:
    #     print(node.key, node.degree)
    #     node = node.sibling
