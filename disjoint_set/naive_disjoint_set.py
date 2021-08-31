from disjoint_set import DisjointSet


class NaiveDisjointSet(DisjointSet):
    def __init__(self, n):
        self.n = n
        self.parent = [x for x in range(n)]

    def find(self, x):
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        self.parent[x_root] = y_root
