from z import get_z_values


def get_spxi(s):
    N = 128
    n = len(s)

    spxi = [[0 for _ in range(n)] for _ in range(N)]

    z = get_z_values(s)

    l = n - 1
    while l > 0:
        r = l + z[l] - 1
        x = s[z[l]]
        spxi[ord(x)][r] = z[l]
        l -= 1

    return spxi


def test_get_spxi():
    spxi = get_spxi("abaabac")
    assert spxi[ord("a")] == [0, 0, 0, 0, 0, 3, 0]
    assert spxi[ord("b")] == [0, 0, 1, 0, 0, 1, 0]
    assert spxi[ord("c")] == [0, 0, 0, 0, 0, 0, 0]


def get_spix(s):
    n = len(s)

    spix = [[] for _ in range(n)]

    z = get_z_values(s)

    l = n - 1
    while l > 0:
        r = l + z[l] - 1
        x = s[z[l]]
        if z[l] > 0:
            spix[r].append((x, z[l]))
        l -= 1

    return spix


def test_get_spix():
    spix = get_spix("abaabac")
    assert spix[0] == []
    assert spix[1] == []
    assert spix[2] == [("b", 1)]
    assert spix[3] == []
    assert spix[4] == []
    assert spix[5] == [("b", 1), ("a", 3)]
    assert spix[6] == []


def get_matches(pattern, text):
    m = len(pattern)
    n = len(text)

    spix = get_spix(pattern)

    def get_sp(i, j):
        if j < n:
            x = text[j]
            spx = spix[i - 1]

            for y, sp in reversed(spx):
                if x == y:
                    return sp

        return 0

    matches = []

    i = 0
    j = 0
    while j < n:
        if pattern[i] == text[j]:
            i += 1
            j += 1

            if i == m:
                matches.append(j - i)

                i = get_sp(i, j)

        else:
            if i == 0:
                j += 1

            else:
                i = get_sp(i, j)

    return matches
