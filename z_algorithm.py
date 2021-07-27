def z_algorithm(s):
    m = len(s)
    z = m * [0]
    l = 0
    r = 0

    for i in range(1, m):
        # Case 1:
        if i > r:
            j = i
            while j < m and s[j - i] == s[j]:
                j += 1
            z[i] = j - i

            if z[i] > 0:
                l = i
                r = i + z[i]

        # Case 2:
        else:
            # Case 2a:
            if z[i - l] < r - i:
                z[i] = z[i - l]

            # Case 2b:
            else:
                j = r
                while j < m and s[j - i] == s[j]:
                    j += 1
                z[i] = j - i

                l = i
                r = i + z[i]

    return z


DELIMITER = "$"


def find(pattern, text):
    assert DELIMITER not in pattern
    assert DELIMITER not in text

    m = len(pattern)
    n = len(text)

    s = pattern + DELIMITER + text
    z = z_algorithm(s)

    matches = []

    for i in range(m + 1, m + n + 1):
        if z[i] == m:
            matches.append(i - m - 1)

    return matches


if __name__ == "__main__":
    print(find("aba", "bbabaxababay"))
    print(find("geek", "geeks for geeks"))
