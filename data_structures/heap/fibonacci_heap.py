from __future__ import annotations
from collections.abc import Iterator
from math import log2
from random import Random
from typing import Any, Generic, Optional

from heap import MIN_COMPARATOR, Comparator, Element, Node
from priority_queue import PriorityQueue


class FibonacciNode(Generic[Element]):
    element: Element
    left: FibonacciNode[Element]
    right: FibonacciNode[Element]

    degree: int = 0
    mark: bool = False
    parent: Optional[FibonacciNode[Element]] = None
    child: Optional[FibonacciNode[Element]] = None

    def __init__(self, element: Element):
        self.element = element
        self.left = self
        self.right = self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.element})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.element})"

    def _cascading_cut(self, head: FibonacciNode[Element]):
        parent = self.parent
        if parent:
            if self.mark:
                self._cut(parent, head)
                parent._cascading_cut(head)
            else:
                self.mark = True

    def _cut(self, parent: FibonacciNode[Element], head: FibonacciNode[Element]):
        parent.degree -= 1

        sibling = self.right
        has_sibling = self is not sibling

        if has_sibling:
            parent.child = sibling
        else:
            parent.child = None

        self.mark = False
        self.parent = None

        self._remove()
        head._merge(self)

    def _iter_elements(self) -> Iterator[Element]:
        for node in self._iter_nodes():
            yield node.element

    def _iter_nodes(self) -> Iterator[FibonacciNode[Element]]:
        for node in self._iter_siblings():
            yield node

            if node.child:
                yield from node.child._iter_nodes()

    def _iter_siblings(self) -> Iterator[FibonacciNode[Element]]:
        stop = self.left

        while True:
            next = self.right

            yield self

            if self is stop:
                break

            self = next

    def _link(self, parent: FibonacciNode[Element]):
        self._remove()

        self.mark = False

        if parent.child:
            parent.child._merge(self)
        else:
            parent.child = self

        self.parent = parent

    def _merge(self, other: FibonacciNode[Element]):
        self_end = self.left
        other_end = other.left

        self_end.right = other
        other_end.right = self

        self.left = other_end
        other.left = self_end

    def _remove(self):
        self.left.right = self.right
        self.right.left = self.left

        self.left = self
        self.right = self


# NOTE: How to enforce the implementation of a Protocol...
# https://github.com/python/mypy/issues/8235
_node: Node[Any] = FibonacciNode[Any](None)


class FibonacciHeap(Generic[Element]):
    """
    Concrete data structure
    Fibonacci heap
    https://en.wikipedia.org/wiki/Fibonacci_heap
    """

    # BUG: Cannot assign to a field of type Callable...
    # https://github.com/python/mypy/issues/708
    # comparator: Comparator[Element]

    head: Optional[FibonacciNode[Element]] = None
    size: int = 0

    def __contains__(self, object: object) -> bool:
        for element in self:
            if element is object:
                return True

        return False

    def __iter__(self) -> Iterator[Element]:
        if not self.head:
            return

        yield from self.head._iter_elements()

    def __init__(self, *, comparator: Comparator[Element] = MIN_COMPARATOR):
        self.comparator = comparator

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.head}, {self.size})"

    def __str__(self) -> str:
        return self.__repr__()

    def _consolidate(self):
        if not self.head:
            return

        max_degree = int(log2(self.size))
        array: list[Optional[FibonacciNode[Element]]] = [None] * (max_degree + 1)

        for node in self.head._iter_siblings():
            node.parent = None

            while True:
                equal_node = array[node.degree]

                if not equal_node:
                    break

                if not self.comparator(node.element, equal_node.element):
                    node, equal_node = equal_node, node

                equal_node._link(node)

                array[node.degree] = None

                node.degree += 1

            array[node.degree] = node

            if not self.comparator(self.head.element, node.element):
                self.head = node

    def decrease_node(self, node: FibonacciNode[Element], element: Element):
        assert not self.comparator(node.element, element)

        if not self.head:
            return

        node.element = element

        parent = node.parent
        if parent and self.comparator(node.element, parent.element):
            node._cut(parent, self.head)
            parent._cascading_cut(self.head)

        if self.comparator(node.element, self.head.element):
            self.head = node

    def delete_node(self, node: FibonacciNode[Element]):
        if not self.head:
            return

        parent = node.parent
        if parent:
            node._cut(parent, self.head)
            parent._cascading_cut(self.head)

        self.head = node
        self.pop()

    def merge(self, other: FibonacciHeap[Element]):
        if not self.head:
            self.head = other.head
            self.size = other.size

        else:
            if not other.head:
                return

            self.head._merge(other.head)

            if not self.comparator(self.head.element, other.head.element):
                self.head = other.head

            self.size += other.size

        other.head = None
        other.size = 0

    def peek(self) -> Optional[Element]:
        node = self.peek_node()

        if not node:
            return None

        return node.element

    def peek_node(self) -> Optional[FibonacciNode[Element]]:
        if not self.head:
            return None

        return self.head

    def pop(self) -> Optional[Element]:
        node = self.pop_node()

        if not node:
            return None

        return node.element

    def pop_node(self) -> Optional[FibonacciNode[Element]]:
        node = self.head

        if not node:
            return None

        if node.child:
            node._merge(node.child)

        sibling = node.right
        has_sibling = node is not sibling

        node._remove()

        if has_sibling:
            self.head = sibling
            self._consolidate()
        else:
            self.head = None

        self.size -= 1

        return node

    def push(self, element: Element):
        node = FibonacciNode(element)

        self.push_node_unsafe(node)

    def push_node(self, node: FibonacciNode[Element]):
        node.degree = 0
        node.mark = False
        node.parent = None
        node.child = None

        self.push_node_unsafe(node)

    def push_node_unsafe(self, node: FibonacciNode[Element]):
        if self.head:
            self.head._merge(node)

            if not self.comparator(self.head.element, node.element):
                self.head = node

        else:
            self.head = node

        self.size += 1


# EXAMPLE: How to enforce the implementation of a Protocol...
# https://github.com/python/mypy/issues/8235
# FEATURE: However, at the moment you cannot define associated types in a Protocol...
# https://github.com/python/typing/issues/548
# https://github.com/python/mypy/issues/7790
# _heap: Heap[Any] = FibonacciHeap[Any]()

# EXAMPLE: How to enforce the implementation of a Protocol...
# https://github.com/python/mypy/issues/8235
_priority_queue: PriorityQueue[Any] = FibonacciHeap[Any]()


_SMALL_SIZE = 10
_LARGE_SIZE = 1000

_RANDOM_SEED = 42


def test_bool_empty():
    heap = FibonacciHeap[int]()

    if heap:
        assert False


def test_bool_one():
    heap = FibonacciHeap[int]()

    heap.push(1)

    if not heap:
        assert False


def test_contains_int():
    heap = FibonacciHeap[int]()

    heap.push(1)

    assert 1 in heap


def test_contains_list():
    heap = FibonacciHeap[list]()

    list_a = [1, 2]
    list_b = [3, 4]
    list_c = [5, 6]

    heap.push(list_a)
    heap.push(list_b)

    assert list_a in heap
    assert list_b in heap
    assert list_c not in heap


def test_decrease_node():
    heap = FibonacciHeap[int]()

    node_a = FibonacciNode(5)
    node_b = FibonacciNode(6)
    node_c = FibonacciNode(7)
    node_d = FibonacciNode(8)
    node_e = FibonacciNode(9)

    heap.push_node(node_a)
    heap.push_node(node_b)
    heap.push_node(node_c)
    heap.push_node(node_d)
    heap.push_node(node_e)

    heap._consolidate()

    heap.decrease_node(node_e, 4)

    assert node_e.element == 4
    assert heap.peek() == 4

    heap.decrease_node(node_d, 3)

    assert node_d.element == 3
    assert heap.peek() == 3


def test_delete_node():
    heap = FibonacciHeap[int]()

    node_a = FibonacciNode(5)
    node_b = FibonacciNode(6)
    node_c = FibonacciNode(7)
    node_d = FibonacciNode(8)
    node_e = FibonacciNode(9)

    heap.push_node(node_a)
    heap.push_node(node_b)
    heap.push_node(node_c)
    heap.push_node(node_d)
    heap.push_node(node_e)

    heap._consolidate()

    assert heap.size == 5

    heap.delete_node(node_c)
    assert heap.size == 4
    assert node_c.element not in heap

    heap.delete_node(node_a)
    assert heap.size == 3
    assert node_a.element not in heap


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
