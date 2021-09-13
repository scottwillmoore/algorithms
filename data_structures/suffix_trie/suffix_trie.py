TERMINAL = "\x00"
ASCII_LEN = 128


class SuffixTrie:
    class Node:
        def __init__(self):
            self.children = [None for _ in range(ASCII_LEN)]

        def __str__(self, depth=0):
            result = []
            indent = depth * "  "

            for k, child in enumerate(self.children):
                if child:
                    x = chr(k)
                    result.append(indent + x)
                    result.append(child.__str__(depth=depth + 1))

            return "\n".join(result)

    def __init__(self, string):
        self.root = self.Node()

        for i in range(len(string)):
            parent = self.root
            for j in range(i, len(string)):
                x = string[j]
                k = ord(x)

                if not parent.children[k]:
                    parent.children[k] = self.Node()

                parent = parent.children[k]

    def __str__(self, depth=0):
        return self.root.__str__()

    def contains(self, string):
        parent = self.root
        for i in range(len(string)):
            x = string[i]
            k = ord(x)

            if not parent.children[k]:
                return False

            parent = parent.children[k]

        return True


if __name__ == "__main__":
    suffix_tree = SuffixTrie("abcab")
    print(suffix_tree)
    print(suffix_tree.contains("ab"))
    print(suffix_tree.contains("abb"))
