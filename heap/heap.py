from abc import ABC, abstractmethod


class Heap(ABC):
    @abstractmethod
    def decrease_key(self, i):
        pass

    @abstractmethod
    def delete(self, i):
        pass

    @abstractmethod
    def extract_min(self):
        pass

    @abstractmethod
    def find_min(self):
        pass

    @abstractmethod
    def insert(self, x):
        pass

    @abstractmethod
    def merge(self, other):
        pass
