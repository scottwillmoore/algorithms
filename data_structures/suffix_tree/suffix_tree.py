# https://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english

ASCII_SYMBOLS = 128

TERMINAL_CHARACTER = "\x00"


class Node:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.children = [None for _ in range(ASCII_SYMBOLS)]


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.children = [None for _ in range(ASCII_SYMBOLS)]

        n = len(self.text)
        for i, x in enumerate(self.text):
            if self.children[ord(x)]:
                None
            else:
                self.children[ord(x)] = Node(i, n)
                print(self.text[i:])


# Construction:
# - Naive algorithm
# - Ukkonen's algorithm

if __name__ == "__main__":
    suffix_tree = SuffixTree("abcabz")
