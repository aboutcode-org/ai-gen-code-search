# -*- coding: utf-8 -*-
#

# Copyright (c) AboutCode.org and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://aboutcode.org for more information about AboutCode FOSS projects.
#

"""
===========================
  Chunking module
===========================

Utilities to chunk and select content chunk using ngrams and hailstorm.
"""

from binascii import crc32
from itertools import islice


def ngrams(iterable, ngram_length):
    """
    Return an iterable of ngrams of length `ngram_length` given an `iterable` of strings.
    Each ngram is a tuple of `ngram_length` items.

    The returned iterable is empty if the input iterable contains less than
    `ngram_length` items.

    Note: this is a fairly arcane but optimized way to compute ngrams.

    For example:

    >>> list(ngrams([1,2,3,4,5], 2))
    [(1, 2), (2, 3), (3, 4), (4, 5)]

    >>> list(ngrams([1,2,3,4,5], 4))
    [(1, 2, 3, 4), (2, 3, 4, 5)]

    >>> list(ngrams([1,2,3,4], 2))
    [(1, 2), (2, 3), (3, 4)]

    >>> list(ngrams([1,2,3], 2))
    [(1, 2), (2, 3)]

    >>> list(ngrams([1,2], 2))
    [(1, 2)]

    >>> list(ngrams([1], 2))
    []

    This also works with arrays or tuples:

    >>> from array import array
    >>> list(ngrams(array('h', [1,2,3,4,5]), 2))
    [(1, 2), (2, 3), (3, 4), (4, 5)]

    >>> list(ngrams(tuple([1,2,3,4,5]), 2))
    [(1, 2), (2, 3), (3, 4), (4, 5)]
    """
    return zip(*(islice(iterable, i, None) for i in range(ngram_length)))


def select_ngrams(ngrams, with_pos=False):
    """
    Return an iterable as a subset of a sequence of ngrams using the hailstorm
    algorithm. If `with_pos` is True also include the starting position for the
    ngram in the original sequence.

    Definition from the paper: http://www2009.eprints.org/7/1/p61.pdf ::

        The algorithm first fingerprints every token and then selects a shingle s
        if the minimum fingerprint value of all k tokens in s occurs at the first
        or the last position of s (and potentially also in between). Due to the
        probabilistic properties of Rabin fingerprints the probability that a
        shingle is chosen is 2/k if all tokens in the shingle are different.

    For example:

    >>> list(select_ngrams([(2, 1, 3), (1, 1, 3), (5, 1, 3), (2, 6, 1), (7, 3, 4)]))
    [(2, 1, 3), (1, 1, 3), (5, 1, 3), (2, 6, 1), (7, 3, 4)]

    Positions can also be included. In this case, tuple of (pos, ngram) are returned:

    >>> list(select_ngrams([(2, 1, 3), (1, 1, 3), (5, 1, 3), (2, 6, 1), (7, 3, 4)], with_pos=True))
    [(0, (2, 1, 3)), (1, (1, 1, 3)), (2, (5, 1, 3)), (3, (2, 6, 1)), (4, (7, 3, 4))]

    This works also from a generator:

    >>> list(select_ngrams(x for x in [(2, 1, 3), (1, 1, 3), (5, 1, 3), (2, 6, 1), (7, 3, 4)]))
    [(2, 1, 3), (1, 1, 3), (5, 1, 3), (2, 6, 1), (7, 3, 4)]
    """
    last = None
    for pos, ngram in enumerate(ngrams):
        nghs = []
        for ng in ngram:
            if isinstance(ng, str):
                ng = bytearray(ng, encoding="utf-8")
            else:
                ng = bytearray(str(ng).encode("utf-8"))
            # FIXME: use a proper hash
            nghs.append(crc32(ng) & 0xFFFFFFFF)
        min_hash = min(nghs)
        if with_pos:
            ngram = (
                pos,
                ngram,
            )
        # keep the ngram whose min hash
        # appears in first or last position in the ngram
        if min_hash in (nghs[0], nghs[-1]):
            yield ngram
            last = ngram
        else:
            # always yield the first or last ngram too.
            if pos == 0:
                yield ngram
                last = ngram
    if last != ngram:
        yield ngram
