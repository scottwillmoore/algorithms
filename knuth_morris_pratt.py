from z import get_z_values


def get_sp_values(s):
    n = len(s)

    sp = [0] * n

    z = get_z_values(s)

    l = n - 1
    while l >= 0:
        r = l + z[l] - 1
        sp[r] = z[l]
        l -= 1

    return sp


def get_matches(pattern, text):
    m = len(pattern)
    n = len(text)

    sp = get_sp_values(pattern)

    matches = []

    j = 0
    while j + (m - 1) < n:
        i = 0
        while i < m and pattern[i] == text[i + j]:
            i += 1

        if i == m:
            matches.append(j)
            j += m - 1
        else:
            j += i - (sp[i] - 1)

    return matches


if __name__ == "__main__":
    print("The Knuth-Morris-Pratt algorithm")

    print(get_matches("aba", "bbabaxababay"))
    print(get_matches("geek", "geeks for geeks"))
