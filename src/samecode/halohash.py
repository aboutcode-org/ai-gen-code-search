#
# Copyright (c) AboutCode, nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/matchcode-toolkit for support or download.
# See https://aboutcode.org for more information about AboutCode FOSSprojects.
#
"""
===========================
  Halo Hash module
===========================

Halo is a family of hash functions that have the un-common property that mostly similar -- but not
identical -- inputs will hash to very similar outputs. This type of hash function is sometimes
called a locality-sensitive hash function, because it is sensitive to the locality of the data being
hashed.

The purpose of these hashes is to quickly compare a large number of elements that are likely to be
similar to find candidates and then compute a more comprehensive similarity only on the candidates.
This includes goals such as identifying near-duplicates of things or to group very similar things
together (a.k.a. clustering), as well as to detect similarities between inputs or perform quick
comparisons under a certain threshold.

For a traditional 'good' hash function, small changes in the input will yield very different hash
outputs (through diffusion and avalanche effect). For instance, cryptographic hashes such as SHA1 or
MD5 behave this way. If you hash two bit strings with a SHA1 function and there is only one bit of
difference between these two strings then the resulting hashes will be rather different. On average,
each time one bit is added to the input, good hash functions have half of the output bits switched
from 0 to 1.

A Halo hash instead hashes similar inputs to the same hash or to a hash that differs only by a few
bits. The similarity between two hashes becomes an approximation of the similarity between the two
original inputs. This simalarity is computed using the hamming distance or number of non-matching
bits between two hashes outputs bit straings. This hamming distance is roughly proportional to the
similarity between the two original inputs and can be used to estimate the similarity of inputs
without having access to these full input.

The Halo name is a play on what one of the hashing function does: a halo is like a fuzzy, halo'ish
representation of the input.

The bit average function ressembles Charikar's algorithm by using each bits in an array of hashes
but does not use a TF/IDF resulting in a simpler procedure.


Halo hashes come in a few varieties:

Bucketed:
---------

The bucket hashes are based on hashing each feature in the input, then grouping the hash by high
bits, similar to a hash table buckets. The number of high bits will determine the size of the
resulting hash (i.e. 8 high bits will yield a 256 positions hash). The set of low bits of hashes in
a hash group is then further processed to yield a single bit. This is a form of content
partitioning.


Bit-averaged:
-------------

The bit averaged hashes use bit positions averaging. It starts by hashing each feature in the input.
The size of these hashes determines the size of the resulting hash. (i.e. a 128 bits hash function
will yield a 128 bits hash). The hashes are assembled in a bit matrix. For each column in the
matrix, bits are summed over and averaged, where the average is the mean (0.5) to yield a 0 or 1 bit
for that column position in the output bit string. This is the the variant that provides the best
results and is implemented here.

Bucketed and bit-averaged:
--------------------------

This is a combination of bucketing where each bucket is bit-averaged. Its starts with bucketing
procedure, then the low bits in each bucket are are transformed in a Bit Average hash. The final
hash is the concatenation of each bucket bit average hash. If a bucket is empty, then the bit
average hash for this bucket is a sequence of 0 as long as the number of low bits considered for the
hash.


Matching and similarity computation:
------------------------------------

The interest of halo hashes is that they can be used as a proxy for simpler similarity comparison
between two inputs. The size reduction allows for a reduction of the space required for doing the
comparison. The fixed size of each hash further helps to optimize the computations required.

For an exact similarity scoring, the hamming distance (bitwise XOR) of every pair of hashes should
be computed. This requires O(n^2) comparisons with n being the number of hashes. This is not
attractive, even with reduction in size.

Yet, there are known techniques to optimize and reduce number of comparisons either by using
replicated lookup tables or using prefix matching. For instance, say you create a 384 bit (48 bytes)
Bit Average hash, split the hash in 12 32bits chunks. Create a hash table using each 32bit chunk as
key and the full hash as value. It can be proven that hashes that share at least one 32 bit chunk
have 11 or less bits in common. So the matching procedure could be: lookup in the hash table, then
for each hash match found, compute a full distance comparison if you want exact results (e.g. edit
distance, hamming distance, etc).

There a few other recent techniques that provide similar and improve matching usually referred to as
"similarity joins" or "all-pairs".

Averaging halo hashes that work on single bits positions (Bucket average, Bit Average) also have the
uncommon property that parts of the hashes can be used as approximation for the longer hash with
decreasing accuracy and therefore that the accuracy of hash matching can be tuned after hashing.

For instance , with a 512 bits bit average hash, you could use the first 32 bits or last 64 bits for
doing initial crude exact matches, then doing a pair wise hamming distance computation but only for
the smaller number of matching pairs. This ability to have a multiple resolution based on how many
bits you use in matching can be useful, at the cost of a reduction in accuracy.

For the bucket hash, the matching is can be based on hash table lookups, where the key contains the
individual hashes of each buckets in a hash, and the value contains the the full hash. Having one or
a few bucket hash matched is usually enough to consider the pair of inputs as near duplicates.

Also halo hashes can be combined in a resulting hash, and further enhanced with additional
information such as a few bits from the previous or next input features, the number of elements that
have been hashed or the size of the input, either for further disambiguation when using short
hashes, or to avoid doing less interesting comparisons between input that have significantly
different sizes.

The Halo name is a play on what one of the hashing function does. A bucket averaging hash keeps a
bit based on the average of the sum of low hash bits grouped by high bits, so the process can be
summarized as: "group by High bits , Average LOw bits" and this gives the HALO acronym. Also a Halo
name seems to fit quite well: these hash functions create some kind of fuzzy halo around the input
through averaging.

Some similar or alternative techniques and functions include:
- Broder et al. minhashing
- Moses Charikar Simhash using random projections and rounding
- Bill Pugh hashtable checksums

The bucket average function resembles Pugh's algorithm by using hash bucketing, but is different
from its usage of only of high and low hash bits, the usage or averages of buckets, and the bit
arrays that are used for hamming distance comparisons instead of checksums.

The bit average function resemble Charikar's algorithm by using each bits in an array of hashes, but
is somewhat different in the way bits are averaged, and the fact a TF/IDF weighting is not used,
resulting in a simpler procedure.

Note that halo hashes are not restricted to a feature vector input, and can use rolling hashes
(shingles) or straight hashes equally well. Charikar's design is for instance geared towards the
document vector space model and requires a global term (the TF/IDF) whereas these hashes do not.
"""

import binascii

from bitarray import bitarray
from bitarray.util import count_xor
from commoncode import codec
from commoncode import hash as commoncode_hash


class BitAverageHaloHash:
    """
    A bit matrix averaging hash.

    The high level processing sketch looks like this:
    For an input of::

        ['this' ,'is', 'a', 'rose', 'great']:

    * we first hash each list item to get something like::

        [4, 15, 2, 12, 12]

    (for instance with a very short hash function of 4 bits output)

    or as bits this would be something like this::

        ['0011',
         '1110',
         '0010',
         '1100',
         '1100']

    * we sum up each bit positions/columns together::

        ['0011',
         '1110',
         '0010',
         '1100',
         '1100']
         -------
          3331

    or stated otherwise: pos1=3, pos2=3, pos3=3, pos4=1

    * The mean value for a column is number of hashes/2 (2 because we use bits).
      Here mean = 5 hashes/2 = 2.5

    * We compare the sum of each position with the mean and yield a bit::

        if pos sum > mean yield 1 else yield 0
            position1 = 3 > mean = 2.5 , then bit=1
            position2 = 3 > mean = 2.5 , then bit=1
            position3 = 3 > mean = 2.5 , then bit=1
            position4 = 1 < mean = 2.5 , then bit=0

    * We build a hash by concatenating the resulting bits::

         pos 1 + pos2 + pos3 + pos4 = '1110'

    In general, this hash seems to show a lower accuracy and higher sensitivity
    with small string and small inputs variations than the bucket average hash.
    But it works better on shorter inputs.

    Some usage examples:

    >>> z = b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()
    >>> a = BitAverageHaloHash(z, size_in_bits=256)
    >>> len(a.digest())
    32
    >>> z = b'''The value specified for size must be no
    ... more larger than the smallest bit vector possible for intVal'''.split()
    >>> b = BitAverageHaloHash(z, size_in_bits=256)
    >>> a.distance(b)
    57
    >>> b.distance(a)
    57
    >>> a = BitAverageHaloHash(size_in_bits=160)
    >>> z = [a.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()]
    >>> assert a.hexdigest() == b'2c10223104c43470e10b1157e6415b2f730057d0'
    >>> b = BitAverageHaloHash(size_in_bits=160)
    >>> z = [b.update(x) for x in b'''The value specified for size must be no
    ... more larger than the smallest bit vector possible for intVal'''.split()]
    >>> assert b.hexdigest() == b'2c912433c4c624e0b03b34576641df8fe00017d0'
    >>> a.distance(b)
    29
    >>> a = BitAverageHaloHash(size_in_bits=128)
    >>> z =[a.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()]
    >>> assert a.hexdigest() == b'028b1699c0c5310cd1b566a893d12f10'
    >>> b = BitAverageHaloHash(size_in_bits=128)
    >>> z = [b.update(x) for x in b'''The value specified for size must be no
    ... more larger than the smallest bit vector possible for intVal'''.split()]
    >>> assert b.hexdigest() == b'0002969060d5b344d1b7602cd9e127b0'
    >>> a.distance(b)
    27
    >>> a = BitAverageHaloHash(size_in_bits=64)
    >>> z = [a.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()]
    >>> assert a.hexdigest() == b'028b1699c0c5310c'
    >>> b = BitAverageHaloHash(size_in_bits=64)
    >>> z = [b.update(x) for x in b'''The value specified for size must be no
    ... more larger than the smallest bit vector possible for intVal'''.split()]
    >>> assert b.hexdigest() == b'0002969060d5b344'
    >>> a.distance(b)
    14
    >>> a = BitAverageHaloHash(size_in_bits=32)
    >>> z = [a.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()]
    >>> b = BitAverageHaloHash(size_in_bits=32)
    >>> z = [b.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible by intVal'''.split()]
    >>> a.distance(b)
    5
    >>> a = BitAverageHaloHash(size_in_bits=512)
    >>> z = [a.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible for intVal'''.split()]
    >>> b = BitAverageHaloHash(size_in_bits=512)
    >>> z = [b.update(x) for x in b'''The value specified for size must be at
    ... least as large as for the smallest bit vector possible by intVal'''.split()]
    >>> a.distance(b)
    46
    """

    # TODO: Keep state, keep 1 position per column

    # TODO: create method to aggregate multiple BitAverageHaloHashes together
    # TODO: refactor this, don't keep all hashes
    # TODO: keep only a list of columns
    def __init__(self, msg=None, size_in_bits=128):
        self.size_in_bits = size_in_bits
        self.columns = [0] * size_in_bits
        self.elements_count = 0

        # TODO: pick one hash module instead of selecting from multiple hash modules
        self.hashmodule = lambda x: x
        try:
            # TODO: pick one hash algorithm
            self.hashmodule = commoncode_hash.get_hasher(size_in_bits)
        except Exception as e:
            raise Exception(
                "No available hash module for the requested "
                "hash size in bits: %(size_in_bits)d" % locals()
            ) from e
        self.update(msg)

    @property
    def digest_size(self):
        """
        Digest size in bytes.
        """
        return self.size_in_bits // 8

    def update(self, msg):
        """
        Append a bytestring or sequence of bytestrings to the hash.
        """
        if not msg:
            return
        if isinstance(
            msg,
            (
                list,
                tuple,
            ),
        ):
            for m in msg:
                self.__hashup(m)
        else:
            self.__hashup(msg)

    def __hashup(self, msg):
        assert isinstance(msg, bytes)
        hsh = self.hashmodule(msg).digest()
        bits = bitarray_from_bytes(hsh)
        normalized = (-1 if v else 1 for v in bits)
        for i, column in enumerate(normalized):
            self.columns[i] += column
        self.elements_count += 1

    def hexdigest(self):
        """
        Return the hex-encoded hash value.
        """
        return binascii.hexlify(self.digest())

    def b64digest(self):
        """
        Return a base64 "url safe"-encoded string representing this hash.
        """
        return codec.b64encode(self.digest())

    def digest(self):
        """
        Return a binary string representing this hash.
        """
        flattened = [1 if col > 0 else 0 for col in self.columns]
        bits = bitarray(flattened)
        return bits.tobytes()

    def distance(self, other):
        """
        Return the bit Hamming distance between this hash and another hash.
        """
        return int(count_xor(self.hash(), other.hash()))

    def hash(self):
        """
        Return this hash as a bitarray.
        """
        return bitarray_from_bytes(self.digest())

    @classmethod
    def combine(cls, hashes):
        """
        Return a BitAverageHaloHash by summing and averaging the columns of the
        BitAverageHaloHashes in `hashes` together, putting the resulting
        columns into a new BitAverageHaloHash and returning it
        """
        size_in_bits = hashes[0].size_in_bits
        for h in hashes:
            assert isinstance(
                hash, cls
            ), "all hashes should be a BitAverageHaloHash, not {}".format(type(h))
            assert h.size_in_bits == size_in_bits

        all_columns = [h.columns for h in hashes]
        b = cls()
        b.columns = [sum(col) for col in zip(*all_columns)]
        return b


def bitarray_from_bytes(b):
    """
    Return a bitarray built from a byte string b.
    """
    a = bitarray()
    a.frombytes(b)
    return a


def byte_hamming_distance(b1, b2):
    """
    Return the Hamming distance between ``b1`` and ``b2`` byte strings
    """
    b1 = binascii.unhexlify(b1)
    b2 = binascii.unhexlify(b2)
    b1 = bitarray_from_bytes(b1)
    b2 = bitarray_from_bytes(b2)
    return hamming_distance(b1, b2)


def hamming_distance(bv1, bv2):
    """
    Return the Hamming distance between ``bv1`` and ``bv2``  bitvectors as the number of equal bits
    for all positions. (e.g. the count of bits set to one in an XOR between two bit strings.)

    ``bv1`` and ``bv2`` must both be  either hash-like Halohash instances (with a hash() function)
    or bitarray instances (that can be manipulated as-is).

    See http://en.wikipedia.org/wiki/Hamming_distance

    For example:

    >>> b1 = bitarray('0001010111100001111')
    >>> b2 = bitarray('0001010111100001111')
    >>> hamming_distance(b1, b2)
    0
    >>> b1 = bitarray('11110000')
    >>> b2 = bitarray('00001111')
    >>> hamming_distance(b1, b2)
    8
    >>> b1 = bitarray('11110000')
    >>> b2 = bitarray('00110011')
    >>> hamming_distance(b1, b2)
    4
    """
    return int(count_xor(bv1, bv2))


def slices(s, size):
    """
    Given a sequence s, return a sequence of non-overlapping slices of ``size``.
    Raise an AssertionError if the sequence length is not a multiple of ``size``.

    For example:

    >>> slices([1, 2, 3, 4, 5, 6], 2)
    [(1, 2), (3, 4), (5, 6)]
    >>> slices([1, 2, 3, 4, 5, 6], 3)
    [(1, 2, 3), (4, 5, 6)]
    >>> try:
    ...    slices([1, 2, 3, 4, 5, 6], 4)
    ... except AssertionError:
    ...    pass
    """
    length = len(s)
    assert length % size == 0, (
        "Invalid slice size: len(%(s)r) is not a multiple of %(size)r" % locals()
    )
    # TODO: time alternative
    # return [s[index:index + size] for index in range(0, length, size)]
    chunks = [iter(s)] * size
    return list(zip(*chunks))


def common_chunks_from_hexdigest(h1, h2, chunk_bytes_length=4):
    """
    Compute the number of common chunks of byte length ``chunk_bytes_length`` between two
    strings ``h1`` and ``h2``, each representing a BitAverageHaloHash hexdigest value.

    For example:

    >>> a = '1f22c2c871cd70521211b138cd76fc04'
    >>> b = '1f22c2c871cd7852121bbd38c576bc84'
    >>> common_chunks_from_hexdigest(a, b, 32)
    1

    Note: `a` and `b` start with the same 8 characters, where the next groups
    of 8 have a few characters off:

    >>> byte_hamming_distance(a, b)
    8
    """
    h1 = bitarray_from_bytes(bytes(binascii.unhexlify(h1)))
    h2 = bitarray_from_bytes(bytes(binascii.unhexlify(h2)))
    h1_slices = slices(h1, chunk_bytes_length)
    h2_slices = slices(h2, chunk_bytes_length)
    commons = (1 for h1s, h2s in zip(h1_slices, h2_slices) if h1s == h2s)
    return sum(commons)


def common_chunks(h1, h2, chunk_bytes_length=4):
    """
    Compute the number of common chunks of byte length ``chunk_bytes_length`` between to
    hashes ``h1`` and ``h2`` using their digest.

    Note that chunks that are all set to zeroes are matched too: they are be
    significant such as empty buckets of bucket hashes.

    For example:

    >>> m1 = b'The value specified for size must be at least as large'.split()
    >>> m2 = b'The value specific for size must be at least as large'.split()
    >>> a = BitAverageHaloHash(msg=m1, size_in_bits=256)
    >>> b = BitAverageHaloHash(msg=m2, size_in_bits=256)
    >>> common_chunks(a, b, 2)
    1
    >>> byte_hamming_distance(a.hexdigest(), b.hexdigest())
    32
    """
    h1_slices = slices(h1.digest(), chunk_bytes_length)
    h2_slices = slices(h2.digest(), chunk_bytes_length)
    commons = (1 for h1s, h2s in zip(h1_slices, h2_slices) if h1s == h2s)
    return sum(commons)


def bit_to_num(bits):
    """
    Return an int (or long) for a bitarray.
    """
    return int(bits.to01(), 2)


def decode_vector(b64_str):
    """
    Return a bit array from an encoded string representation.
    """
    decoded = codec.urlsafe_b64decode(b64_str)
    return bitarray_from_bytes(decoded)
