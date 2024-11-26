==================================================
Data Structure Design for efficient index search
==================================================


Our design is that fingerprints are matched approximately using the hamming distance as metric.

We document here an approach and design for efficient storage and matching of indexed data under a
hamming distance threshold.

The core design to index fingerprints represented as their bit strings is to divide your hash bit
string in several chunks and query on these chunks as an exact match or lookup.

This is a "pre-filter" step. Then we can perform a bitwise hamming distance computation on the
returned results which should be only a smaller subset of the overall indexed dataset. This can be
done using data files or SQL tables.

Our design is to use a database table. The fingerpint length we selected is typically 128 bits to
512 bits. The examples here are with 32 bits for simplicity:

Say we have a bunch of 32 bits hashes in the DB and that we want to find every hash that are within
a 4 bits hamming distance of our "query" hash:

1. We create a table with four columns: each will contain an 8 bits (as a string or int) slice of
   the 32 bits hashes, islice1 to islice4.

2. We slice our query hash the same way in qslice1 to qslice4.

3. We query this table such that any of these clauses are true:
   `qslice1=islice1 or qslice2=islice2 or qslice3=islice3 or qslice4=islice4`

  This gives us every DB hash that are within 3 bits (`4 - 1`) of the query hash. It may contain
  more results, and this is why there is a step 4.

4. For each returned hash, we then compute the exact hamming distance pair-wise with our query hash
   (reconstructing the index-side hash from the four slices)


The number of operations in step 4 should be much less than a full pair-wise hamming computation of
our whole table.


An standard implementation documented in the litterature is to use sorted files where you permute
the chunks (or slices) as described in [MANKU]. This is a design that can work well when you have
a large cluster of machines usable for map-reduce type jobs. Our alternative is to reuse a standard
relational database table instead and this provides several benefits beyond the basic use case of
mere near-duplicate detection:

1. We can store additional data for each match which are essential since we need to account for the
   actual origin of a match
2. We can do live updates, which are hard to impossible with the sorted file based approach

The overall slicing approach was first described afaik by Moses Charikar in its "simhash" seminal
paper [CHARIKAR]::

    5. APPROXIMATE NEAREST NEIGHBOR SEARCH IN HAMMING SPACE

    [...]

    Given bit vectors consisting of d bits each, we choose N = O(n 1/(1+ ) ) random permutations of
    the bits. For each random permutation σ, we maintain a sorted order O σ of the bit vectors, in
    lexicographic order of the bits permuted by σ. Given a query bit vector q, we find the
    approximate nearest neighbor by doing the following:

    For each permutation σ, we perform a binary search on O σ to locate the two bit vectors closest
    to q (in the lexicographic order obtained by bits permuted by σ). We now search in each of the
    sorted orders O σ examining elements above and below the position returned by the binary search
    in order of the length of the longest prefix that matches q.


Monika Henziger expanded on this in her paper [HENZIGER]::

    3.3 The Results for Algorithm C

    We partitioned the bit string of each page into 12 non-overlapping 4-byte pieces, creating 20B
    pieces, and computed the C-similarity of all pages that had at least one piece in common. This
    approach is guaranteed to find all pairs of pages with difference up to 11, i.e., C-similarity
    373, but might miss some for larger differences.


Note: Here the C-similarity is the same as the Hamming distance: The Hamming distance is the number
of positions at which the corresponding bits differ while C-similarity is the number of positions at
which the corresponding bits agree.


In addition we had a private communication with Monica Henzinger who kindly clarified the procedure
principles::

    -------- Original Message --------
    Subject: Question on hamming distance matching above a treshold
    From: Philippe Ombredanne
    To: Monika Henzinger

    Hello Monika:

    First le me tell you that I am a big fan of your research, especially in the domain of near
    duplicates.

    In the paper: "Finding Near-Duplicate Web Pages:A Large-Scale Evaluation of Algorithms" you state:

    "3.3 The Results for Algorithm C
    We partitioned the bit string of each page into 12 non- overlapping 4-byte pieces, creating 20B
    pieces,and com- puted the C-similarity of all pages that had at least one piece in common."

    Then you claim:

    "This approach is guaranteed to find all pairs of pages with difference up to 11, i.e.,
    C-similarity 373, but might miss some for larger differences."

    My question: what would be a sketch of a proof for this claim?
    And how I could generalize this to other minimal hamming distances, pieces
    size and length of the bit string?

    Thanks for your kind consideration
    --
    Cordially
    Philippe


    Subject: Re: Question on hamming distance matching above a treshold
    From: Monika Henzinger
    To: Philippe Ombredanne

    I broke the page into x pieces (x = 12).
    Now I find all pages that agree in at least one piece and compute their C-similarity.
    Assume the difference between 2 pages A and B is y, with y < x.
    Then there must exist at least one of the x pieces that are the same in both A and B,
    since y differences can cause at most y different pieces,
    thus the remaining x - y >= 1 pieces must be identical.
    Since I compute the C-similarity for all pages with at least 1 identical piece,
    I will compute the C-similarity for A and B.
    If however A and B would differ in z >= x pieces,
    then it could be that ALL of the x pieces into which I broke A and B differ.
    Thus I might not compute their C-similarity because A and B do not agree on even a single piece.
    I hope that explains it and shows you how to generalize it.
    Monika


This hamming distance matching method is also explained in this paper [MANKU]::

    3. THE HAMMING DISTANCE PROBLEM

    Definition: Given a collection of f -bit fingerprints and a
    query fingerprint F, identify whether an existing fingerprint
    differs from F in at most k bits. (In the batch-mode version
    of the above problem, we have a set of query fingerprints
    instead of a single query fingerprint)

    [...]
    Intuition: Consider a sorted table of 2 d f -bit truly random fingerprints.
    Focus on just the most significant d bits in the table. A listing of these d-bit numbers amounts
    to “almost a counter” in the sense that (a) quite a few 2 d bit- combinations exist, and (b)
    very few d-bit combinations are duplicated. On the other hand, the least significant f − d bits
    are “almost random”.

    Now choose d such that |d − d| is a small integer. Since the table is sorted, a single probe
    suffices to identify all fingerprints which match F in d most significant bit-positions. Since
    |d − d| is small, the number of such matches is also expected to be small. For each matching
    fingerprint, we can easily figure out if it differs from F in at most k bit-positions or not
    (these differences would naturally be restricted to the f − d least-significant bit-positions).

    The procedure described above helps us locate an existing fingerprint that differs from F in k
    bit-positions, all of which are restricted to be among the least significant f − d bits of F.
    This takes care of a fair number of cases. To cover all the cases, it suffices to build a small
    number of additional sorted tables, as formally outlined in the next Section.


References
-------------------

- [CHARIKAR] Similarity Estimation Techniques from Rounding Algorithms
  https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf

- [HENZIGER] Finding near-duplicate web pages: A large-scale evaluation of algorithms
  https://infoscience.epfl.ch/record/99373/files/Henzinger06.pdf

- [MANKU] Detecting Near-Duplicates for Web Crawling
  https://research.google.com/pubs/archive/33026.pdf
