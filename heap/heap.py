from abc import ABC, abstractmethod


class Heap(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def find_min(self):
        pass

    @abstractmethod
    def extract_min(self):
        pass
