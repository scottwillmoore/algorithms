def get_z_values(s):
    n = len(s)

    z = [0] * n

    l = 0
    r = 0

    i = 1
    while i < n:
        if i > r:
            j = 0
            while i + j < n and s[j] == s[i + j]:
                j += 1

            if j > 0:
                l = i
                r = i + j - 1

            z[i] = j

        else:
            if i + z[i - l] > r:
                j = r - i + 1
                while i + j < n and s[j] == s[i + j]:
                    j += 1

                l = i
                r = i + j - 1

                z[i] = j

            else:
                z[i] = z[i - l]

        i += 1

    return z


def test_get_z_values():
    assert get_z_values("abxabxxx") == [0, 0, 0, 3, 0, 0, 0, 0]
    assert get_z_values("bbccaebbcabd") == [0, 1, 0, 0, 0, 0, 3, 1, 0, 0, 1, 0]
    assert get_z_values("aabcaabxaay") == [0, 1, 0, 0, 3, 1, 0, 0, 2, 1, 0]


DELIMITER = "\x00"


def get_matches(pattern, text):
    m = len(pattern)
    n = len(text)

    s = pattern + DELIMITER + text

    z = get_z_values(s)

    matches = []

    i = m + 1
    while i < m + n + 1:
        if z[i] == m:
            matches.append(i - m - 1)

        i += 1

    return matches


def test_get_matches():
    assert get_matches("aba", "bbabaxababay") == [2, 6, 8]
    assert get_matches("geek", "geeks for geeks") == [0, 10]
