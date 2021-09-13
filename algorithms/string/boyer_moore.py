def extended_bad_character(text):
    m = len(text)

    r = [[] for _ in range(128)]

    for j in reversed(range(m)):
        x = text[j]
        r[ord(x)].append(j)

    return r


def z_algorithm(text):
    m = len(text)

    z = [0 for _ in range(m)]

    l = 0
    r = 0
    for i in range(1, m):
        if i > r:
            j = i
            while j < m and text[j - i] == text[j]:
                j += 1
            z[i] = j - i

            if z[i] > 0:
                l = i
                r = i + z[i]

        else:
            if z[i - l] < r - i:
                z[i] = z[i - l]

            else:
                j = r
                while j < m and text[j - i] == text[j]:
                    j += 1
                z[i] = j - i

                l = i
                r = i + z[i]

    return z


def boyer_moore(pattern, text):
    p = []

    m = len(pattern)
    n = len(text)

    r = extended_bad_character(pattern)

    reversed_pattern = pattern[::-1]
    z = z_algorithm(reversed_pattern)[::-1]
    print(z)

    i = 0
    while i < n - m:
        j = m - 1
        while j >= 0:
            x = text[i + j]
            y = pattern[j]

            if x != y:
                break

            j -= 1

        if j == -1:
            p.append(i)
            i += m - 1
        else:
            o = 1
            for s in r[ord(x)]:
                if s < j:
                    o = j - s
                    break
            i += o

    return p


if __name__ == "__main__":
    print(boyer_moore("aba", "bbabaxababay"))
    print(boyer_moore("geek", "geeks for geeks"))
    print(boyer_moore("acababacaba", "acxcbbacabacabaa"))
