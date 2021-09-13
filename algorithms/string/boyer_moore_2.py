# https://en.wikipedia.org/wiki/ASCII
# https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm
# https://www.inf.hs-flensburg.de/lang/algorithmen/pattern/bmen.htm
# https://www.youtube.com/watch?v=lkL6RkQvpMM


# N  = Alphabet length
#
# P  = Pattern
# m  = Pattern length
# i  = Pattern index
# x  = Pattern character
#
# T  = Text
# n  = Text length
# j  = Text index
# y  = Text character
#
# R  = Bad character table
# Rk = Extended bad character table
# Rl = Efficient extended bad character table
#
# Zs = Z suffix table
# Gs = Good suffix table
# Mp = Matched prefix table
#
# M  = Matches


N = 128


# Get the bad character table
# Time: O(m), Space: O(N)
def get_R(P):
    m = len(P)

    R = [-1 for _ in range(N)]

    i = 0
    while i < m:
        x = P[i]
        R[ord(x)] = i

        i += 1

    return R


# Get the extended bad character table
# Time: O(m^2), Space: O(N*m)
def get_Rk(P):
    m = len(P)

    Rk = [[-1 for _ in range(N)] for _ in range(m)]

    k = 0
    while k < m:
        i = 0
        while i < k:
            x = P[i]
            Rk[k][ord(x)] = i

            i += 1

        k += 1

    return Rk


# Get the efficient extended bad character table
# Time: O(m), Space: O(N)
def get_Rl(P):
    m = len(P)

    Rl = [[] for _ in range(N)]

    i = m - 1
    while i >= 0:
        x = P[i]
        Rl[ord(x)].append(i)

        i -= 1

    return Rl


# Get the Z table
# Time: O(m), Space: O(m)
def get_Z(P):
    m = len(P)

    Z = [0 for _ in range(m)]

    l = 0
    r = 0
    for i in range(1, m):
        if i > r:
            j = i
            while j < m and P[j - i] == P[j]:
                j += 1
            Z[i] = j - i

            if Z[i] > 0:
                l = i
                r = i + Z[i]

        else:
            if Z[i - l] < r - i:
                Z[i] = Z[i - l]

            else:
                j = r
                while j < m and P[j - i] == P[j]:
                    j += 1
                Z[i] = j - i

                l = i
                r = i + Z[i]

    return Z


# Get the Z suffix table
# Time: O(m), Space: O(m)
def get_Zs(P):
    return get_Z(P[::-1])[::-1]


# Get the good suffix table
# Time: O(m), Space: O(m)
def get_Gs(P):
    m = len(P)

    Zs = get_Zs(P)
    print("Zs", Zs)

    Gs = [0 for _ in range(m)]

    p = 0
    while p < m:
        i = m - Zs[p] - 1
        Gs[i] = p
        p += 1

    return Gs


# Get the matched prefix table
# Time: O(m), Space: O(m)
def get_Mp(P):
    m = len(P)

    Mp = [0 for _ in range(m)]

    return Mp


# Find occurrences of P in T
# Time: O(m + n), Space: O(m + n)
def boyer_moore(P, T):
    print("P", P)
    print("T", T)

    M = []

    m = len(P)
    n = len(T)

    Rk = get_Rk(P)

    Gs = get_Gs(P)
    print("Gs", Gs)

    Mp = get_Mp(P)
    print("Mp", Mp)

    j = 0
    while j < n - m:
        i = m - 1
        while i >= 0:
            x = P[i]
            y = T[j + i]

            if x != y:
                break

            i -= 1

        if i == -1:
            M.append(j)
            j += m - 1
        else:
            j += i - Rk[i][ord(y)]

    return M


if __name__ == "__main__":
    print(boyer_moore("aba", "bbabaxababay"))
    print(boyer_moore("geek", "geeks for geeks"))
    print(boyer_moore("acababacaba", "acxcbbacabacabaa"))
