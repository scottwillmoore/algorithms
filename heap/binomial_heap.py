from heap import Heap, Node


# class BinomialHeap(Heap, Node):
class BinomialHeap:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None

    def merge(self, other):
        assert isinstance(self, BinomialHeap)
        assert isinstance(other, BinomialHeap)

        head = None
        if self.degree < other.degree:
            head = self
            self = self.sibling
        else:
            head = other
            other = other.sibling

        current = head
        while True:
            if self.degree < other.degree:
                current.sibling = self
                current = self
                self = self.sibling

                if not self:
                    current.sibling = other
                    break

            else:
                current.sibling = other
                current = other
                other = other.sibling

                if not other:
                    current.sibling = self
                    break

        previous = None
        current = head
        next = current.sibling

        # I think there is a chance that their way is a bit more ugly.
        # I think there is a nicer way...

        while True:
            # Case 1:
            if current.degree != next.degree:
                previous = current
                current = next
                next = next.sibling

            # Case 2:

            # Case 3:
            previous = current
            current = current.sibling
            next = current.sibling

        if current.degree == next.degree:
            # MERGE
            pass

        return head


if __name__ == "__main__":
    h1 = BinomialHeap(12)
    h1.sibling = BinomialHeap(7)
    h1.sibling.degree = 1
    h1.sibling.sibling = BinomialHeap(15)
    h1.sibling.sibling.degree = 2

    h2 = BinomialHeap(18)
    h2.sibling = BinomialHeap(3)
    h2.sibling.degree = 1
    h2.sibling.sibling = BinomialHeap(6)
    h2.sibling.sibling.degree = 4

    node = h1.merge(h2)
    # node = h2.merge2(h1)
    while node:
        print(node.key, node.degree)
        node = node.sibling
