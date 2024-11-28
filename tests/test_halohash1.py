#
# Copyright (c) AboutCode.org and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
from pathlib import Path

from commoncode.codec import num_to_bin
from commoncode.testcase import FileDrivenTesting

from samecode import halohash

test_env = FileDrivenTesting()
test_env.test_data_dir = str((Path(__file__).parent / "testfiles").absolute())


class TestHalohash:

    def test_BitAverageHaloHash_simple(self):
        a = halohash.BitAverageHaloHash(None, size_in_bits=512)
        [a.update(num_to_bin(x)) for x in range(4096)]
        expected = (
            b"df38b3eddba771b5e6ddeb0851c6651c95d26bd5e8"
            b"944c10125cd50968759927c51238fb83d0ff4de5f6a0"
            b"c05de0837d00f6e47c4a880592f1c87b175df5db15"
        )
        assert a.hexdigest() == expected

    def test_BitAverageHaloHash_elements_count_unicode_ticket_2785(self):
        a = halohash.BitAverageHaloHash(None, size_in_bits=512)
        [a.update(num_to_bin(x)) for x in range(4096)]
        assert a.elements_count == 4096

    def _random_HaloHash_test(self, size_in_bits, chunk_size):
        """
        Using two files created with dd from a Linux /dev/urandom as an input,
        this test split each file in chunks. A halohash is computed over the
        chunks and the hamming distance is computed for each file. The second
        files is progressively injected one chunk at a time from the first
        file, mimicking a gradual buildup of similarity
        """
        # the two random files are exactly 70000 bytes... use a chunk size that
        # is a divider of it
        assert 70000 % chunk_size == 0

        random1 = test_env.get_test_loc("random/random1.txt")
        random2 = test_env.get_test_loc("random/random2.txt")

        def chunks(seq, n):
            """
            Return a sequence of contiguous non-overlapping chunks of size n.
            """
            return [seq[i : i + n] for i in range(len(seq))[::n]]

        content1 = open(random1, "rb").read()
        chunks1 = chunks(content1, chunk_size)
        halo1 = halohash.BitAverageHaloHash(size_in_bits=size_in_bits)
        for x in chunks1:
            halo1.update(x)

        content2 = open(random2, "rb").read()
        chunks2 = chunks(content2, chunk_size)

        results = []
        for i in range(len(chunks1)):
            # create a new halohash on the second list
            halo2 = halohash.BitAverageHaloHash(size_in_bits=size_in_bits)
            for chunk in chunks2:
                halo2.update(chunk)
            # compare with the original under bit hamming distance
            results.append((i, halo1.distance(halo2)))
            # replace one chunk to mimic similarity buildup
            chunks2[i] = chunks1[i]

        return results

    def test_random_BitAverageHaloHash(self):
        result = self._random_HaloHash_test(size_in_bits=256, chunk_size=1000)
        expected = [
            (0, 140),
            (1, 137),
            (2, 133),
            (3, 128),
            (4, 126),
            (5, 129),
            (6, 127),
            (7, 127),
            (8, 121),
            (9, 117),
            (10, 116),
            (11, 114),
            (12, 116),
            (13, 116),
            (14, 109),
            (15, 114),
            (16, 110),
            (17, 110),
            (18, 112),
            (19, 105),
            (20, 111),
            (21, 107),
            (22, 102),
            (23, 104),
            (24, 100),
            (25, 102),
            (26, 100),
            (27, 96),
            (28, 93),
            (29, 98),
            (30, 97),
            (31, 93),
            (32, 90),
            (33, 86),
            (34, 82),
            (35, 80),
            (36, 78),
            (37, 79),
            (38, 74),
            (39, 76),
            (40, 80),
            (41, 76),
            (42, 72),
            (43, 69),
            (44, 71),
            (45, 73),
            (46, 65),
            (47, 66),
            (48, 63),
            (49, 58),
            (50, 55),
            (51, 54),
            (52, 52),
            (53, 47),
            (54, 49),
            (55, 47),
            (56, 44),
            (57, 45),
            (58, 44),
            (59, 44),
            (60, 47),
            (61, 42),
            (62, 32),
            (63, 34),
            (64, 29),
            (65, 30),
            (66, 27),
            (67, 29),
            (68, 24),
            (69, 9),
        ]

        assert result == expected
