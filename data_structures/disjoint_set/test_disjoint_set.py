from pytest import fixture

from naive_disjoint_set import NaiveDisjointSet
from union_by_height_disjoint_set import UnionByHeightDisjointSet
from union_by_rank_disjoint_set import UnionByRankDisjointSet
from union_by_size_disjoint_set import UnionBySizeDisjointSet


DisjointSets = [NaiveDisjointSet, UnionByHeightDisjointSet, UnionByRankDisjointSet, UnionBySizeDisjointSet]


@fixture(params=DisjointSets)
def DisjointSet(request):
    return request.param


# https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/UnionFind.pdf
def test_princeton_university(DisjointSet):
    disjoint_set = DisjointSet(10)

    disjoint_set.union(3, 8)
    disjoint_set.union(4, 8)
    disjoint_set.union(9, 8)

    for x in [3, 4, 9]:
        assert disjoint_set.find(8) == disjoint_set.find(x)

    disjoint_set.union(1, 5)
    disjoint_set.union(6, 5)

    disjoint_set.union(0, 7)
    disjoint_set.union(5, 7)
    disjoint_set.union(2, 7)

    for x in [0, 1, 2, 5, 6]:
        assert disjoint_set.find(7) == disjoint_set.find(x)

    disjoint_set.union(7, 8)

    for x in range(10):
        assert disjoint_set.find(0) == disjoint_set.find(x)
