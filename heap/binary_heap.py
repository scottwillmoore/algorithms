from heap import Heap


class BinaryHeap(Heap):
    def __init__(self, array):
        self.array = array
        self.__heapify()

    def __bool__(self):
        return bool(self.array)

    def __len__(self):
        return len(self.array)

    def __heapify(self):
        for i in reversed(range(len(self) // 2 + 1)):
            self.__sift_down(i)

    def __sift_down(self, i):
        while True:
            child = 2 * i
            if child < len(self):
                next_child = child + 1
                if next_child < len(self) and self.array[next_child] < self.array[child]:
                    child = next_child

                if self.array[child] < self.array[i]:
                    self.__swap(child, i)
                    i = child
                else:
                    break
            else:
                break

    def __sift_up(self, i):
        while True:
            parent = i // 2
            if parent >= 0:
                if self.array[i] < self.array[parent]:
                    self.__swap(i, parent)
                    i = parent
                else:
                    break
            else:
                break

    def __swap(self, i, j):
        assert 0 <= i < len(self), 0 <= j < len(self)
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def decrease_key(self, i, x):
        assert 0 <= i < len(self)
        assert x < self.array[i]
        self.array[i] = x
        self.__sift_up(i)

    def delete(self, i):
        assert 0 <= i < len(self)
        x = self.array[i]
        self.__swap(i, len(self) - 1)
        self.array.pop()
        if self.array[i] < x:
            self.__sift_up(i)
        else:
            self.__sift_down(i)

    def extract_min(self):
        assert 0 < len(self)
        x = self.array[0]
        self.__swap(0, len(self) - 1)
        self.array.pop()
        self.__sift_down(0)
        return x

    def find_min(self):
        assert 0 < len(self)
        return self.array[0]

    def insert(self, x):
        self.array.append(x)
        self.__sift_up(len(self) - 1)

    def merge(self, other):
        self.array + other.array
        self.__heapify()


if __name__ == "__main__":
    heap = BinaryHeap([5, 9, 2, 4, 3, 8, 6, 7, 1])

    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
    print(heap.extract_min())
