# -*- coding: utf-8 -*-
#
# Copyright (c) AboutCode, nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/matchcode-toolkit for support or download.
# See https://aboutcode.org for more information about AboutCode FOSSprojects.
#

from unittest.case import TestCase

from samecode.chunking import ngrams
from samecode.chunking import select_ngrams


class TestNgrams(TestCase):

    def test_ngrams(self):
        tokens = """
            Redistribution and use in source and binary are permitted.
            """.split()

        result = list(ngrams(tokens, ngram_length=4))
        expected = [
            ("Redistribution", "and", "use", "in"),
            ("and", "use", "in", "source"),
            ("use", "in", "source", "and"),
            ("in", "source", "and", "binary"),
            ("source", "and", "binary", "are"),
            ("and", "binary", "are", "permitted."),
        ]
        assert result == expected

    def test_ngrams_with_None(self):
        tokens = [
            "Redistribution",
            "and",
            "use",
            None,
            "in",
            "source",
            "and",
            "binary",
            "are",
            None,
        ]
        result = list(ngrams(tokens, ngram_length=4))
        expected = [
            ("Redistribution", "and", "use", None),
            ("and", "use", None, "in"),
            ("use", None, "in", "source"),
            (None, "in", "source", "and"),
            ("in", "source", "and", "binary"),
            ("source", "and", "binary", "are"),
            ("and", "binary", "are", None),
        ]
        assert result == expected

    def test_ngrams_with_None_length_three(self):
        tokens = [
            "Redistribution",
            "and",
            "use",
            None,
            "in",
            "source",
            "and",
            "binary",
            "are",
            None,
        ]
        result = list(ngrams(tokens, ngram_length=3))
        expected = [
            ("Redistribution", "and", "use"),
            ("and", "use", None),
            ("use", None, "in"),
            (None, "in", "source"),
            ("in", "source", "and"),
            ("source", "and", "binary"),
            ("and", "binary", "are"),
            ("binary", "are", None),
        ]
        assert result == expected

    def test_ngrams2(self):
        tokens = """
            Redistribution and use in source and binary are permitted.
            """.split()

        result = list(ngrams(tokens, ngram_length=4))
        expected = [
            ("Redistribution", "and", "use", "in"),
            ("and", "use", "in", "source"),
            ("use", "in", "source", "and"),
            ("in", "source", "and", "binary"),
            ("source", "and", "binary", "are"),
            ("and", "binary", "are", "permitted."),
        ]

        assert result == expected

    def test_select_ngrams_with_unicode_inputs(self):
        result = list(
            select_ngrams(
                x
                for x in [
                    ("b", "ä", "c"),
                    ("ä", "ä", "c"),
                    ("e", "ä", "c"),
                    ("b", "f", "ä"),
                    ("g", "c", "d"),
                ]
            )
        )
        expected = [
            ("b", "ä", "c"),
            ("ä", "ä", "c"),
            ("e", "ä", "c"),
            ("b", "f", "ä"),
            ("g", "c", "d"),
        ]
        assert result == expected
