===================================================================
  Design for Modified Approximate Code search with Code Stemming
===================================================================

Early testing showed that two pieces of code that uses the overall same code flow may not be
detected as approximately similar if all the variable names are different.

When this happens, the selected content chunks may have different boundaries and/or the fingerprints
computed on these fragments may have significantly different values.

Because of this we need to design a new approach. The key to this new design will be to pre-process
code using token replacements to abtract the token and keyword representation to a "conceptual"
value. This approach is an application of the more text common "stemming" [STEMMING] used to
pre-process terms to their "stem" in a search engine, but applied to source code::

    From Wikipedia, the free encyclopedia

    In linguistic morphology and information retrieval, stemming is the
    process of reducing inflected (or sometimes derived) words to their word
    stem, base or root form—generally a written word form. The stem need not
    be identical to the morphological root of the word; it is usually
    sufficient that related words map to the same stem, even if this stem is
    not in itself a valid root. Algorithms for stemming have been studied in
    computer science since the 1960s. Many search engines treat words with
    the same stem as synonyms as a kind of query expansion, a process called
    conflation.

    A computer program or subroutine that stems word may be called a
    stemming program, stemming algorithm, or stemmer.

This approach applied to software programs is a technique developed in [GRUNE] where code is pre-
processed and code tokens are replaced by an abstract value. We call this "Code Stemming".

Described by Dick Grune in 1989 in [GRUNE1989], it consists roughly of these steps:

- Given a source code file, determine the programming language of the source file, based on its
  file name, file extension or content in our case using for instance the ``typecode`` library

- For each programming language, create a list of keywords, instructions or strings that are
  associated with this programming language. Eventually map each of these to a smaller string or
  code.

- Given a file's programming language, we then either replace text that matches a a keyword using
  its mapped value, or remove text that does not match these keywords list for this programming
  language. This replaces each keyword and programing construct of the original source file with a
  compact representation encoded as a sequence of mapped codes. This effectively transforms the code
  in a simplified, abstract tokens stream. The detection of the keywords to replace could be based
  on parsing the code or even just perform a lighter lexing to identify code tokens to lookup their
  replacement. With this approach it is also possible to remove unknown code segments, and comments.
  This are the elements that are not known in the lists and mappings.

For instance an "if" instruction may be replaced by a "i" for conditional; or an "index" variable or
class name may be replaced by a "V" for variable. This pre-processing will takes place before actual
chunking the content and fingerprinting, and with it, code that is essentially similar will be
abstracted to its essence, ignoring naming styles and preferences.

The description given in [GRUNE1989] is this::

    This program reads the code to be examined, reduces the text to a string
    of 8-bits “essential tokens”, and then repeatedly finds the longest
    common non-overlapping substring. [...] The criteria for the reduction
    to essential tokens are programmed in a replaceable module in the
    similarity tester. They usually involve reducing all identifiers and
    numbers to a single token, <idf>, all strings to a single <string>, all
    characters to <char>, removing all comment and lay- out, and replacing
    each keyword of the pro- gramming language by a separate token.

The provided [GRUNE] code contains extensive description and implementation of the principles, such
as this mapping of C lanuages identifiers to a short one character code (in SIM's file clang.l)::

    static const struct idf ppcmd[] = {
        {"define",    META('d')},
        {"else",    META('e')},
        {"endif",    META('E')},
        {"if",        META('i')},
        {"ifdef",    META('I')},
        {"ifndef",    META('x')},
        {"include",    MTCT('I')},
        {"line",    META('l')},
        {"undef",    META('u')}
    };

The benefits of this improved design is that approximate search becomes impervious to changes
in variables and identifier names: this captures the essence of the code without complex code
parsing or comtrol flow analysis.


References
---------------

- [STEMMING] Stemming
  https://en.wikipedia.org/wiki/Stemming

- [GRUNE] The software and text similarity tester SIM
  https://www.dickgrune.com/Programs/similarity_tester/index.html and
  https://web.archive.org/web/19970606165903/http://www.cs.vu.nl/~dick/sim.html

- [GRUNE1989] Detecting copied submissions in computer science workshops
  https://www.dickgrune.com/Programs/similarity_tester/Paper.pdf
