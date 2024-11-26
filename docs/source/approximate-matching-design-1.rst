==================================================================
 Content Chunking and Fingerprint design for Approximate search
==================================================================


This document details a key element of our design for efficient approximate similar software code
discovery and identification at scale.

The design for matching approximate software code consists of these three elements:

1. Content-defined chunking algorithm to split code into fragments and select a subset of these
   fragments

2. Fingerprinting fragments with a locality sensitive hashing (LSH) function for approximate
   matching of these fragments. This fingerprint can embed multiple precision in a single bit
   string to tune the search precision and organize the search in rounds of progressively
   increasing precision.

3. Indexing-time approximate matching for deduplication where each new content fragment is added to
   the index if it is not already matchable approximately in the index, avoiding large duplications
   of indexed entries, which is inherent to the nature of open source code where reuse and vendoring
   is a common thing.

This document details the first two elements, e.g., our approach and design for content-chunking and
fingerprinting.


We first describe the general context and problems we are trying to resolve, and then present the
design itself.


We carefully considered three fingerprinting approaches and two content-defined chunking approaches:

- for content chunking we considered hailstorm and winnowing: we selected a modified hailstorm
  approach.
- for fingerprinting we considered min-wise independent permutations, random projections,
  and hash bucket fingerprinting: we selected random projections

The approach for selecting content is this:

- We normalize text content by normalizing contiguous space and assimilated, lowercasing all words
  and breaking on space and punctuation boundaries to obtain a sequence of tokens.

- We then compute ngrams over this sequence of tokens, using a value of N=5 based on tests and the
  litterature, in particular [BURROWS] to obtain a sequence of ngrams.

- We then move a sliding window over this sequence of ngrams and use the hailstorm procedure. If
  the windows first or last ngram hash is the smallest value, then we select all the ngrams in this
  window.


The approach for fingerprinting using random projections is a sequence of ngrams hashes from the
previous step, to compute their Halohash bit average:

- Transform each hashes in a bitstring, formaing a matrix of bits.
- Sum the bits in each column assigning a value of -1 to 0 and +1 to 1.
- Quantize the column sum values to 1 for positive sums and 0 for negative sums.
- Transfor the resulting bitstring in a binary value. This is the fingerprint


References
-------------------

- [AIKEN] Winnowing: Local Algorithms for Document Fingerprinting
  https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf

- [ABDEL-HAMID] Detecting the origin of text segments efficiently
  https://infoscience.epfl.ch/record/138562/files/OriginTextSegments.pdf

- [SEO] Local Text Reuse Detection
  https://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=812

- [JOHNSON-LINDENSTRAUSS] Johnson-Lindenstrauss lemma
  https://en.wikipedia.org/wiki/Johnson–Lindenstrauss_lemma

- [BRODER] On the resemblance and containment of documents
  https://web.archive.org/web/20150131043133/http://gatekeeper.dec.com/ftp/pub/dec/SRC/publications/broder/positano-final-wpnums.pdf

- [CHARIKAR] Similarity Estimation Techniques from Rounding Algorithms
  https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf

- [HENZIGER] Finding near-duplicate web pages: A large-scale evaluation of algorithms
  https://infoscience.epfl.ch/record/99373/files/Henzinger06.pdf

- [BURROWS] Efﬁcient plagiarism detection for large code repositories
  https://people.eng.unimelb.edu.au/jzobel/fulltext/spe07.pdf

- [SOOD-LOGUINOV] Probabilistic near-duplicate detection using simhash
  https://irl.cse.tamu.edu/people/sadhan/papers/cikm2011.pdf

- [STEIN] Efﬁcient plagiarism detection for large code repositories
  https://downloads.webis.de/publications/papers/stein_2005a.pdf

- [LULU] Overview of fingerprinting methods for local text reuse detection
  https://www.researchgate.net/profile/Boumediene-Belkhouche/publication/310441711_Overview_of_Fingerprinting_Methods_for_Local_Text_Reuse_Detection/links/5bbc8344299bf1049b783ce0/Overview-of-Fingerprinting-Methods-for-Local-Text-Reuse-Detection.pdf

- [JEKABSONS] Evaluation of Fingerprint Selection Algorithms for Local Text Reuse Detection
  http://www.cs.rtu.lv/jekabsons/Files/Jek_ACSS2020.pdf

- [MANKU] Detecting Near-Duplicates for Web Crawling
  https://research.google.com/pubs/archive/33026.pdf

