from __future__ import annotations
from math import log2
from random import Random
from typing import Callable, Generic, Iterator, Optional, TypeVar

from priority_queue import PriorityQueue


_Element = TypeVar("_Element")


class FibonacciNode(Generic[_Element]):
    """
    Concrete data structure
    Fibonacci node
    """

    element: _Element
    left: FibonacciNode[_Element]
    right: FibonacciNode[_Element]

    degree: int = 0
    mark: bool = False
    parent: Optional[FibonacciNode[_Element]] = None
    child: Optional[FibonacciNode[_Element]] = None

    def __init__(self, element: _Element) -> None:
        self.element = element
        self.left = self
        self.right = self

    def __repr__(self) -> str:
        return f"(element={self.element}, degree={self.degree}, mark={self.mark}, left={self.left.element}, right={self.right.element})"

    def __str__(self) -> str:
        return self.__repr__()

    def concatenate(self, other: FibonacciNode[_Element]) -> None:
        self_end = self.left
        other_end = other.left

        self_end.right = other
        other_end.right = self

        self.left = other_end
        other.left = self_end

    def extract(self) -> None:
        self.left.right = self.right
        self.right.left = self.left

        self.left = self
        self.right = self

    # def show(self, depth=0, show_siblings=True) -> None:
    #     indent = ">   " * depth

    #     print(f"{indent}{self}")

    #     if self.child:
    #         self.child.show(depth=depth + 1)

    #     if show_siblings:
    #         next = self.right
    #         while next is not self:
    #             next.show(depth=depth, show_siblings=False)
    #             next = next.right


_Comparator = Callable[[_Element, _Element], bool]


_MIN_COMPARATOR: _Comparator = lambda x, y: x < y


class FibonacciHeap(Generic[_Element]):
    """
    Concrete data structure
    Fibonacci heap
    https://en.wikipedia.org/wiki/Fibonacci_heap
    """

    # https://github.com/python/mypy/issues/708
    # comparator: _Comparator[Element]

    head: Optional[FibonacciNode[_Element]] = None
    size: int = 0

    def __contains__(self, element: object) -> bool:
        pass

    def __iter__(self) -> Iterator[_Element]:
        pass

    def __init__(self, *, comparator: _Comparator[_Element] = _MIN_COMPARATOR) -> None:
        self.comparator = comparator

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(head = {self.head}, size = {self.size})"

    def __str__(self) -> str:
        return self.__repr__()

    def consolidate(self) -> None:
        if not self.head:
            return

        max_degree = int(log2(self.size))
        array: list[Optional[FibonacciNode[_Element]]] = [None] * (max_degree + 1)

        current = self.head
        stop = self.head.left

        while True:
            next = current.right

            x = current
            x.parent = None

            while True:
                y = array[x.degree]

                if not y:
                    break

                if not self.comparator(x.element, y.element):
                    x, y = y, x

                y.extract()
                y.mark = False
                y.parent = x

                if x.child:
                    x.child.concatenate(y)
                else:
                    x.child = y

                array[x.degree] = None
                x.degree += 1

            array[x.degree] = x

            if not self.comparator(self.head.element, x.element):
                self.head = x

            if current is stop:
                break

            current = next

    def decrease_node(self, node: FibonacciNode[_Element]) -> None:
        pass

    def delete_node(self, node: FibonacciNode[_Element]) -> None:
        pass

    def find_node(self, element: _Element) -> Optional[FibonacciNode[_Element]]:
        pass

    def merge(self, other: FibonacciHeap[_Element]) -> None:
        if not self.head:
            self.head = other.head
            self.size = other.size

        else:
            if not other.head:
                return

            self.head.concatenate(other.head)

            if not self.comparator(self.head.element, other.head.element):
                self.head = other.head

            self.size += other.size

        other.head = None
        other.size = 0

    def peek(self) -> Optional[_Element]:
        node = self.peek_node()

        if not node:
            return None

        return node.element

    def peek_node(self) -> Optional[FibonacciNode[_Element]]:
        if not self.head:
            return None

        return self.head

    def pop(self) -> Optional[_Element]:
        node = self.pop_node()

        if not node:
            return None

        return node.element

    def pop_node(self) -> Optional[FibonacciNode[_Element]]:
        node = self.head

        if not node:
            return None

        if node.child:
            node.concatenate(node.child)

        sibling = node.right
        has_sibling = node is not sibling

        node.extract()

        if has_sibling:
            self.head = sibling
            self.consolidate()
        else:
            self.head = None

        self.size -= 1

        return node

    def push(self, element: _Element) -> None:
        node = FibonacciNode(element)

        self.push_node_unsafe(node)

    def push_node(self, node: FibonacciNode[_Element]) -> None:
        node.degree = 0
        node.mark = False
        node.parent = None
        node.child = None

        self.push_node_unsafe(node)

    def push_node_unsafe(self, node: FibonacciNode[_Element]) -> None:
        if self.head:
            self.head.concatenate(node)

            if not self.comparator(self.head.element, node.element):
                self.head = node

        else:
            self.head = node

        self.size += 1


# https://github.com/python/mypy/issues/8235
_priority_queue: PriorityQueue = FibonacciHeap()


_LARGE_SIZE = 10
_SMALL_SIZE = 10


_RANDOM_SEED = 42


def test_merge_empty():
    heap_1 = FibonacciHeap[int]()
    heap_2 = FibonacciHeap[int]()

    heap_1.merge(heap_2)

    assert heap_1.head is None
    assert heap_1.size == 0
    assert heap_2.head is None
    assert heap_2.size == 0


def test_merge_one():
    heap_1 = FibonacciHeap[int]()
    heap_1.push(1)

    heap_2 = FibonacciHeap[int]()
    heap_2.push(2)

    heap_1.merge(heap_2)

    assert heap_1.head.element == 1
    assert heap_1.head.left.element == 2
    assert heap_1.head.right.element == 2
    assert heap_1.size == 2
    assert heap_2.head is None
    assert heap_2.size == 0


def test_merge_two():
    heap_1 = FibonacciHeap[int]()
    heap_1.push(1)
    heap_1.push(2)

    heap_2 = FibonacciHeap[int]()
    heap_2.push(3)
    heap_2.push(4)

    heap_1.merge(heap_2)

    not_min = [2, 3, 4]

    assert heap_1.head.element == 1
    assert heap_1.head.left.element in not_min
    assert heap_1.head.left.left.element in not_min
    assert heap_1.head.left.left.left.element in not_min
    assert heap_1.head.left.left.left.left.element == 1
    assert heap_1.head.right.element in not_min
    assert heap_1.head.right.right.element in not_min
    assert heap_1.head.right.right.right.element in not_min
    assert heap_1.head.right.right.right.right.element == 1
    assert heap_1.size == 4
    assert heap_2.head is None
    assert heap_2.size == 0


def test_peek_empty():
    heap = FibonacciHeap[int]()

    assert heap.peek() is None
    assert heap.size == 0


def test_peek_one():
    heap = FibonacciHeap[int]()
    heap.push(1)

    assert heap.peek() == 1
    assert heap.size == 1


def test_pop_empty():
    heap = FibonacciHeap[int]()

    assert heap.pop() is None
    assert heap.head is None
    assert heap.size == 0


def test_pop_one():
    heap = FibonacciHeap[int]()
    heap.push(1)

    assert heap.pop() == 1
    assert heap.head is None
    assert heap.size == 0


def test_pop_one_with_one_child():
    heap = FibonacciHeap[int]()

    node = FibonacciNode(1)
    node_child = FibonacciNode(2)

    node.child = node_child
    node_child.parent = node

    node.degree = 1

    heap.head = node
    heap.size = 2

    assert heap.pop() == 1
    assert heap.head is node_child
    assert heap.head.degree == 0
    assert heap.head.parent is None
    assert heap.head.child is None
    assert heap.size == 1

    assert heap.pop() == 2
    assert heap.head is None
    assert heap.size == 0


def test_pop_one_with_two_children():
    heap = FibonacciHeap[int]()

    node = FibonacciNode(1)
    node_child_a = FibonacciNode(2)
    node_child_b = FibonacciNode(3)

    node_child_a.parent = node
    node_child_b.parent = node

    node_child_a.left = node_child_b
    node_child_b.left = node_child_a

    node_child_a.right = node_child_b
    node_child_b.right = node_child_a

    node.degree = 2
    node.child = node_child_a

    heap.head = node
    heap.size = 3

    heap.head.show()
    assert heap.pop() == 1
    assert heap.head is node_child_a
    assert heap.head.left is node_child_a
    assert heap.head.right is node_child_a
    assert heap.head.degree == 1
    assert heap.head.parent is None
    assert heap.head.child is node_child_b
    assert heap.head.child.left is node_child_b
    assert heap.head.child.right is node_child_b
    assert heap.size == 2

    assert heap.pop() == 2
    assert heap.head is node_child_b
    assert heap.head.degree == 0
    assert heap.head.parent is None
    assert heap.head.child is None
    assert heap.size == 1

    assert heap.pop() == 3
    assert heap.head is None
    assert heap.size == 0


def test_pop_two():
    heap = FibonacciHeap[int]()
    heap.push(1)
    heap.push(2)

    assert heap.pop() == 1
    assert heap.head.element == 2
    assert heap.size == 1

    assert heap.pop() == 2
    assert heap.head is None
    assert heap.size == 0


def test_push_one():
    heap = FibonacciHeap[int]()
    heap.push(1)

    assert heap.head.element == 1
    assert heap.size == 1


def test_push_two():
    heap = FibonacciHeap[int]()
    heap.push(1)

    assert heap.head.element == 1
    assert heap.size == 1

    heap.push(2)

    assert heap.head.element == 1
    assert heap.head.left.element == 2
    assert heap.head.right.element == 2
    assert heap.size == 2


def test_queue_sequential_small():
    queue: PriorityQueue[int] = FibonacciHeap()

    for i in range(_SMALL_SIZE):
        queue.push(i)

    for i in range(_SMALL_SIZE):
        assert i == queue.pop()


def test_queue_sequential_large():
    queue: PriorityQueue[int] = FibonacciHeap()

    for i in range(_LARGE_SIZE):
        queue.push(i)

    for i in range(_LARGE_SIZE):
        assert i == queue.pop()


def test_queue_random_small():
    data = list(range(_SMALL_SIZE))

    random = Random(_RANDOM_SEED)
    random.shuffle(data)

    queue: PriorityQueue[int] = FibonacciHeap()

    for x in data:
        queue.push(x)

    data.sort()

    for x in data:
        assert x == queue.pop()


def test_queue_random_large():
    data = list(range(_LARGE_SIZE))

    random = Random(_RANDOM_SEED)
    random.shuffle(data)

    queue: PriorityQueue[int] = FibonacciHeap()

    for x in data:
        queue.push(x)

    data.sort()

    for x in data:
        assert x == queue.pop()
