=========================================
  SameCode library
=========================================


``Search, detect, and identify AI-generated code and other copied code.``

The AI-Generated Code Search project provides open source tools to find code that may have been
generated using LLMs and GPT tools.

In this project, SameCode is a low level Python library that exposes features to:

1. Break code content in code fragments
2. Compute fingerprints for approximate matching these fragments
3. Provide related utilities for hamming distance computation

These features are fundamental building blocks for code fragments and snippets matching
approximately.

WARNING: this is under heavy development and not yet a finished project!

Note that using this library alone is not straightforward. Consider looking at the design and
reference documentation at https://ai-gen-code-search.readthedocs.io for more details.
It is designed to be used in the context of a larger code matching feature with MatchCode and the
PurlDB: https://github.com/aboutcode-org/purldb


- PyPI: https://pypi.org/project/samecode/
- Homepage: https://github.com/aboutcode-org/ai-gen-code-search
- Documentation: https://ai-gen-code-search.readthedocs.io

Installation
------------

SameCode is standalone library that does not provide a UI and command line. To install

From PyPI::

  pip install samecode


The preferred development setup is with these commands to create a development environment::

    git clone https://github.com/aboutcode-org/ai-gen-code-search
    cd ai-gen-code-search
    make dev # to configure the environemnt
    make test # to run tests
    make check # to run code checks 


Alternatively, a checkout of the https://github.com/aboutcode-org/ai-gen-code-search repo
can also be installed into an environment using pip's ``--editable`` option ::

    git clone https://github.com/aboutcode-org/ai-gen-code-search
    cd ai-gen-code-search
    python -m venv venv
    venv/bin/pip install --editable .

or built into a wheel and dists and then installed::

    pip install build
    venv/bin/pyproject-build --wheel --sdist
    pip install dist/samecode*.whl


Usage
-------

SameCode provides these functions classes:

In the module  ``samecode.chunking``, the main functions are:

- ``ngrams(iterable, ngram_length)``
  Return an iterable of ngrams of length `ngram_length` given an `iterable` of strings.
  Each ngram is a tuple of `ngram_length` items.
  The returned iterable is empty if the input iterable contains less than
  `ngram_length` items.

- ``select_ngrams(ngrams, with_pos=False)``
  Return an iterable as a subset of a sequence of ngrams using the hailstorm
  algorithm. If `with_pos` is True also include the starting position for the
  ngram in the original sequence.

In the module: ``samecode.halohash``, the main functions and classes are:

- ``BitAverageHaloHash(msg=None, size_in_bits=128)``
     A bit matrix averaging hash object, with these methods and properties:

     ``digest_size``
         Digest size in bytes.

     ``b64digest(self)``
         Return a base64 "url safe"-encoded string representing this hash.

     ``hexdigest(self)``
         Return the hex-encoded hash value.

     ``digest(self)``
         Return a binary string representing this hash.

     ``distance(self, other)``
         Return the bit Hamming distance between this hash and another hash.

     ``hash(self)``
         Return this hash as a bitarray.

     ``update(self, msg)``
         Append a bytestring or sequence of bytestrings to the hash.

     ``BitAverageHaloHash.combine(hashes)`` (class method)
         Return a BitAverageHaloHash by summing and averaging the columns of the
         BitAverageHaloHashes in `hashes` together, putting the resulting
         columns into a new BitAverageHaloHash and returning it

- ``bit_to_num(bits)``
     Return an int (or long) for a bitarray.
 
- ``bitarray_from_bytes(b)``
     Return a bitarray built from a byte string b.
 
- ``byte_hamming_distance(b1, b2)``
     Return the Hamming distance between ``b1`` and ``b2`` byte strings
 
- ``common_chunks(h1, h2, chunk_bytes_length=4)``
     Compute the number of common chunks of byte length ``chunk_bytes_length`` between to
     hashes ``h1`` and ``h2`` using their digest.
 
- ``common_chunks_from_hexdigest(h1, h2, chunk_bytes_length=4)``
     Compute the number of common chunks of byte length ``chunk_bytes_length`` between two
     strings ``h1`` and ``h2``, each representing a BitAverageHaloHash hexdigest value.
 
- ``decode_vector(b64_str)``
     Return a bit array from an encoded string representation.
 
- ``hamming_distance(bv1, bv2)``
     Return the Hamming distance between ``bv1`` and ``bv2``  bitvectors as the number of equal bits
     for all positions. (e.g. the count of bits set to one in an XOR between two bit strings.)
     
     ``bv1`` and ``bv2`` must both be  either hash-like Halohash instances (with a hash() function)
     or bitarray instances (that can be manipulated as-is).
 
- ``slices(s, size)``
     Given a sequence s, return a sequence of non-overlapping slices of ``size``.
     Raise an AssertionError if the sequence length is not a multiple of ``size``.


See also code examples in the test suite under /tests.


Tests
--------

Run the tests with::

    pytest -vvs

or with::

    make test


License
-------

SPDX-License-Identifier: Apache-2.0



Acknowledgements, Funding, Support and Sponsoring
--------------------------------------------------------

|europa|
    
|ngisearch|   

Funded by the European Union. Views and opinions expressed are however those of the author(s) only
and do not necessarily reflect those of the European Union or European Commission. Neither the
European Union nor the granting authority can be held responsible for them. Funded within the
framework of the NGI Search project under grant agreement No 101069364


This project is also supported and sponsored by:

- Generous support and contributions from users like you!
- Microsoft and Microsoft Azure
- AboutCode ASBL


|aboutcode| 


.. |ngisearch| image:: https://www.ngisearch.eu/download/FlamingoThemes/NGISearch2/NGISearch_logo_tag_icon.svg?rev=1.1
    :target: https://www.ngisearch.eu/
    :height: 50
    :alt: NGI logo


.. |ngi| image:: https://ngi.eu/wp-content/uploads/thegem-logos/logo_8269bc6efcf731d34b6385775d76511d_1x.png
    :target: https://www.ngi.eu/ngi-projects/ngi-search/
    :height: 37
    :alt: NGI logo

.. |europa| image:: etc/eu.funded.png
    :target: http://ec.europa.eu/index_en.htm
    :height: 120
    :alt: Europa logo

.. |aboutcode| image:: https://aboutcode.org/wp-content/uploads/2023/10/AboutCode.svg
    :target: https://aboutcode.org/
    :height: 30
    :alt: AboutCode logo
