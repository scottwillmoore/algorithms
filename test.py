from itertools import chain, product, tee

from knuth_morris_pratt_modified import get_matches as knuth_morris_pratt_modified
from knuth_morris_pratt import get_matches as knuth_morris_pratt
from shift_or import get_matches as shift_or
from z import get_matches as z

ALPHABET_START = 97
ALPHABET_STOP = 101

WORD_START = 1
WORD_STOP = 6

TESTS = [knuth_morris_pratt, knuth_morris_pratt_modified, shift_or, z]


def get_matches(pattern, text):
    matches = []

    i = text.find(pattern)
    while i != -1:
        matches.append(i)
        i = text.find(pattern, i + 1)

    return matches


def test_by_example():
    for test in TESTS:
        assert test("aba", "bbabaxababay") == [2, 6, 8]
        assert test("geek", "geeks for geeks") == [0, 10]
        assert test("abxabxxx", "abxababxabxxx") == [5]
        assert test("ababcabab", "ababdabacdababcabab") == [10]


def test_by_brute_force():
    letters = list(map(chr, range(ALPHABET_START, ALPHABET_STOP)))
    products = (product(letters, repeat=i) for i in range(WORD_START, WORD_STOP))
    tuples = chain.from_iterable(products)
    words = map("".join, tuples)
    pairs = product(words, repeat=2)

    for pattern, text in pairs:
        matches = get_matches(pattern, text)
        for test in TESTS:
            assert matches == test(pattern, text)
