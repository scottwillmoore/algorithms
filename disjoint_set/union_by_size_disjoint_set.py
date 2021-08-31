from disjoint_set import DisjointSet


class UnionBySizeDisjointSet(DisjointSet):
    def __init__(self, n):
        self.n = n
        self.parent = [-1 for _ in range(n)]

    def find(self, x):
        while not self.parent[x] < 0:
            x = self.parent[x]
        return x

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)

        if x_root == y_root:
            return

        x_size = -self.parent[x_root]
        y_size = -self.parent[y_root]

        if x_size > y_size:
            self.parent[y_root] = x_root
            self.parent[x_root] = -(x_size + y_size)
        else:
            self.parent[x_root] = y_root
            self.parent[y_root] = -(x_size + y_size)


if __name__ == "__main__":
    disjoint_set = UnionBySizeDisjointSet(10)
    disjoint_set.union(1, 2)
    disjoint_set.union(3, 4)

    print(disjoint_set.find(1))
    print(disjoint_set.find(2))
    print(disjoint_set.find(3))
    print(disjoint_set.find(4))
    print(disjoint_set.find(5))
