from pytest import fixture

from binary_heap import BinaryHeap

Heaps = [BinaryHeap]


@fixture(params=Heaps)
def Heap(request):
    return request.param


def test_sort_10(Heap):
    heap = Heap([5, 9, 2, 4, 3, 8, 1, 6, 7, 0])
    for i in range(10):
        assert i == heap.extract_min()
