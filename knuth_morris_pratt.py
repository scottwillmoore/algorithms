from z import get_z_values


def get_sp_values(s):
    n = len(s)

    sp = [0] * n

    z = get_z_values(s)

    l = n - 1
    while l > 0:
        r = l + z[l] - 1
        sp[r] = z[l]
        l -= 1

    return sp


def test_get_sp_values():
    assert get_sp_values("aba") == [0, 0, 1]
    assert get_sp_values("abxabxxx") == [0, 0, 0, 0, 0, 3, 0, 0]
    assert get_sp_values("bbccaebbcabd") == [0, 1, 0, 0, 0, 0, 0, 1, 3, 0, 1, 0]
    assert get_sp_values("aabcaabxaay") == [0, 1, 0, 0, 0, 1, 3, 0, 0, 2, 0]
    assert get_sp_values("abcd abd ") == [0, 0, 0, 0, 0, 0, 2, 0, 0]
    assert get_sp_values("ab ac ab abc ") == [0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 2, 0, 0]
    assert get_sp_values("abacababa ") == [0, 0, 1, 0, 0, 0, 3, 0, 3, 0]


def get_matches(pattern, text):
    m = len(pattern)
    n = len(text)

    sp = get_sp_values(pattern)

    matches = []

    i = 0
    j = 0
    while j < n:
        if pattern[i] == text[j]:
            i += 1
            j += 1

            if i == m:
                matches.append(j - i)
                i = sp[i - 1]

        else:
            if i == 0:
                j += 1
            else:
                i = sp[i - 1]

    return matches


def test_get_matches():
    assert get_matches("aba", "bbabaxababay") == [2, 6, 8]
    assert get_matches("geek", "geeks for geeks") == [0, 10]
    assert get_matches("abxabxxx", "abxababxabxxx") == [5]
    assert get_matches("ababcabab", "ababdabacdababcabab") == [10]
