from abc import ABC, abstractmethod


class DisjointSet(ABC):
    @abstractmethod
    def __init__(self, n):
        pass

    @abstractmethod
    def find(self, x):
        pass

    @abstractmethod
    def union(self, x, y):
        pass
