from heap import Heap


class BinaryHeap(Heap):
    def __init__(self, array):
        self.array = array
        self.n = len(self.array)

        for i in reversed(range(self.n // 2 + 1)):
            self.__sift_down(i)

    def insert(self, x):
        self.array.append(x)
        self.n = len(self.array)
        self.__sift_up(self.n - 1)

    def find_min(self):
        assert self.n > 0
        return self.array[0]

    def extract_min(self):
        assert self.n > 0

        x = self.array[0]
        self.__swap(0, self.n - 1)

        self.array.pop()
        self.n = len(self.array)
        self.__sift_down(0)

        return x

    def __swap(self, i, j):
        assert i < self.n, j < self.n
        self.array[i], self.array[j] = self.array[j], self.array[i]

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

    def __sift_down(self, i):
        while True:
            child = 2 * i
            if child < self.n:
                next_child = child + 1
                if next_child < self.n and self.array[next_child] < self.array[child]:
                    child = next_child

                if self.array[child] < self.array[i]:
                    self.__swap(child, i)
                    i = child
                else:
                    break
            else:
                break


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
