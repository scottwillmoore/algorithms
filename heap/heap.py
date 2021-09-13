# Heap (data structure)
# [1] https://en.wikipedia.org/wiki/Heap_(data_structure)

from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, key, value=None):
        self.key = key
        self.value = value


class Heap(ABC):
    @abstractmethod
    def decrease_key(self, node, key):
        pass

    @abstractmethod
    def delete(self, node):
        pass

    @abstractmethod
    def extract_min(self):
        pass

    @abstractmethod
    def find_min(self):
        pass

    @abstractmethod
    def insert(self, node):
        pass

    @abstractmethod
    def merge(self, other):
        pass
