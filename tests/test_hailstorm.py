#
# Copyright (c) AboutCode.org and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#
from hashlib import sha1

from commoncode.codec import bin_to_num

from samecode.chunking import ngrams

"""
This is a set of local tests to compare hailstorm with winnowing.
"""


def select_ngrams_with_hailstorm(ngs, hashm):
    """
    Select ngrams using hailstorm

    DEFINITION: from the paper: Hailstorm (Hs)

    The algorithm first fingerprints every token and then selects a shingle s if the minimum
    fingerprint value of all k tokens in s occurs at the first or the last position of s (and
    potentially also in between)

    Due to the probabilistic properties of Rabin fingerprints the probability that a shingle is
    chosen is 2/k if all tokens in the shingle are different.
    """

    ngs = list(ngs)
    # 'fingerprint' each ngram tokens individually
    nghs = [[h.digest() for h in map(hashm, ng)] for ng in ngs]
    selected_ngrams = []
    # iterate over each ngram token hashes tuple
    # iterate over each tuple
    for i in range(len(ngs)):
        ngh = nghs[i]
        min_ngh = min(bin_to_num(h) for h in ngh)
        # keep the ngram whose min token fingerprint
        # appears in first or last position in the ngram
        if ngh[0] == min_ngh or ngh[-1] == min_ngh:
            selected_ngrams.append(ngs[i])
        else:
            # always select the first and last fingerprint
            if i == 0 or i == len(ngs):
                selected_ngrams.append(ngs[i])
    return selected_ngrams


def select_ngrams_with_winnowing(ngs, hashm, window):
    """
    Select ngrams using winnowing

    DEFINITION 3 (ROBUST WINNOWING). In each window select the minimum hash value. If possible break
    ties by selecting the same hash as the window one position to the left. If not, select the
    rightmost minimal hash. Save all selected hashes as the fingerprints of the document.
    """
    ngs = list(ngs)

    # 'fingerprint' all ngram tokens
    nghs = [hashm(b"".join(ng)).digest() for ng in ngs]
    selected_ngrams = []
    nghs = [bin_to_num(b) for b in nghs]

    """iterates over window"""
    last_min = 0
    for i in range(len(nghs) - window + 1):
        win = nghs[i : i + window]
        win_min = min(win)
        win_min_i = win.index(win_min)
        if i == 0:
            selected_ngrams.append(ngs[i + win_min_i])
            last_min = win_min
            continue
        if last_min == win_min:
            continue
        else:
            selected_ngrams.append(ngs[i + win_min_i])
            last_min = win_min

    return selected_ngrams


def other_tokens(ngs, ng):
    allotherng = set()
    for n in ngs:
        if n != ng:
            allotherng.add(tuple(n))
    # create a set of all covered tokens elsewhere
    alltok = set()
    for n in allotherng:
        alltok.update(n)
    return alltok


def discard_covered(ngs):
    """
    Check for coverage and keep covered
    """
    covered = ngs[:]
    for n in ngs:
        tokens = other_tokens(covered, n)
        if all([t in tokens for t in n]):
            covered.remove(n)
    return covered


def discard_covered_neigh1(ngs):
    """
    Discard covered neighbours, 1st variant
    """
    kept = [(x, 1) for x in ngs]
    for i in range(len(ngs)):
        tok = ngs[i]
        previous_neighbours = ngs[i - 1 : i]
        neighbours = [n for n in previous_neighbours if n in kept]
        allnt = []
        for neb in neighbours:
            allnt += neb
        if all([t in allnt for t in tok]):
            kept[i] = (tok, 0)
    return [ng[0] for ng in kept if ng[1] == 1]


def discard_covered_neigh2(ngs):
    """
    Discard covered neighbours, 2nd variant
    """
    # List of tuples: [1] =1 if kept, 0 if to discard
    covered = [(x, 1) for x in ngs]
    for i in range(len(covered)):
        tok = covered[i][0]
        pneib1 = covered[i - 1 : i]
        nneib1 = covered[i + 1 : i + 2]
        pneib2 = covered[i - 2 : i - 1]
        nneib2 = covered[i + 2 : i + 3]
        neib = (
            pneib1[0]
            if len(pneib1) == 2 and pneib1[1]
            else (
                [] + nneib1[0]
                if len(nneib1) == 2 and nneib1[1]
                else (
                    [] + pneib2[0]
                    if len(pneib2) == 2 and pneib2[1]
                    else [] + nneib2[0] if len(nneib2) == 2 and nneib2[1] else []
                )
            )
        )
        if all([t in neib for t in tok]):
            covered[i] = (tok, 0)

    return [c[0] for c in covered if c[1]]


def _uniq(data):
    """
    Return a list of unique elements, keeping the order in which they appear in the input
    """
    # there may be a better way but I can't find it
    output = []
    for elem in data:
        if elem not in output:
            output.append(elem)
    return output


def test_compare_functions():

    sample = (
        """The algorithm first fingerprints every token and
        then selects a shingle s iff the minimum fingerprint
        value of all k tokens in s occurs at the first or
        the last position of s and potentially also
        in-between
        """
        * 10
    )

    tokens = sample.split()
    tokens = [s.encode("utf-8") for s in tokens]
    ngr = ngrams(tokens, 8)
    ngr = list(ngr)

    hsmu = list(select_ngrams_with_hailstorm(ngr, sha1))
    hsmuu = list(_uniq(hsmu))
    hsmud = list(discard_covered(hsmu))

    print("hsmu:", len(ngr), len(hsmuu), len(hsmu), len(hsmud))

    wimu = list(select_ngrams_with_winnowing(ngr, sha1, 32))
    wimud = list(discard_covered(wimu))
    wimuu = list(_uniq(wimu))
    print("wimu:", len(ngr), len(wimuu), len(wimu), len(wimud))
