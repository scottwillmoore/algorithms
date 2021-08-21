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
            if i + z[i - l] < r:
                z[i] = z[i - l]

            else:
                j = z[i - l]
                while i + j < n and s[j] == s[i + j]:
                    j += 1

                l = i
                r = i + j - 1

                z[i] = j

        i += 1

    return z


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


if __name__ == "__main__":
    print("The Z algorithm")

    print(get_matches("aba", "bbabaxababay"))
    print(get_matches("geek", "geeks for geeks"))
