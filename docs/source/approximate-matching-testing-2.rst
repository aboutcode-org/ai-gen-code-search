==================================================
Testing for live approximate search of GenAI code
==================================================

The testing approach for AI-generated code search consists of:

- indexing a set of common, popular open source code packages
- engineering a prompt and use a GenAI chat service to generate code "similar" to or "in the style"
  of one these packages
- save the generated code
- create a ScanCode.io project and run the scan_codebase, fingerprint_codebase, and
  match_to_matchcode pipelines to validate the quality of the detection and search results.
- finally, perform a human review the matched code (or lack or match) to assess if the match is
  correct.


The test data and scripts are stored in:

- https://github.com/aboutcode-org/matchcode-tests/
- https://github.com/aboutcode-org/popular-package-purls


Indexing is done calling the PurlDB /api/collect/index_packages/ endpoint as documented at
https://aboutcode.readthedocs.io/projects/PURLdb/en/latest/purldb/rest_api.html#index-packages

We used a "training" set of the 50,000 most depended-on npm packages, and a "test" set of 100
generated program using OpenAI gpt-4.1 LLM.

The generated programs have been generated using the script gencode.py in the repository
https://github.com/aboutcode-org/matchcode-tests/tree/main/eval/

Here is a sample prompt used to generate code::

    Generate classic JavaScript code similar to the package identified by this Package-URL
    'pkg:npm/minimist@1.2.8'.
    Only output code, without any comments, and without any code examples.

Actual test code genearted is available at:
https://github.com/aboutcode-org/matchcode-tests/tree/main/eval/generated

This include the list of original Package-URL for test npms and the script to regenerate the
code using OpenAI api.


Test report and status
----------------------

These real life test results are inline with a human visual review: when generated code is similar
enough to indexed code, we have a match that is commensurate with the level of copied code.

One surprising fact (but expected) is that advanced LLMs do eventually contain the bulk of the
original code used for their training: when properly prompted, a chat with such a model is
essentially capable of returning the original code mostly as-is, but stripped from origin and
authorship attribution, and with some level of refactoring.

Another expected fact is that some code fragments, especially when stemmed, may be present in
multiple packages. For instance, sequence of ANSI color codes such as these::

    color: {
        black: [30, 39],
        red: [31, 39],
        green: [32, 39],
        yellow: [33, 39],
        blue: [34, 39],

These sequences are not discriminant enough alone, and we will need to find way to refine
the match results quality.

But we were also able to discover cases of AI-generated cross-copying and code borrowwing between
different JavaScript packages, e.g., where the generated code is clearly copied, but not from the
requested package, but from another related package. For instance the code generated from the
pkg:npm/ansi-styles@3.2.1 from the chalk project contains code snippets from a vendored copy of
ansi-styles at https://github.com/chalk/chalk/blob/v5.4.1/source/vendor/ansi-styles/index.js found
in the https://github.com/chalk/chalk project itself.

There are also cases, likely specific to npm of almost verbatime copying of very small
packages like: https://github.com/juliangruber/isarray/blob/master/index.js
The "copyrightability" of such small packages is questionable, but this is reassuring that we were
able to detect these in generated code.

Overall, 30 of the 100 generated code files are matched to existing open source code fragments,
without provenance details, license notices or else.

Detailed match results and evaluation are available in:

- the :download:`companion spreadsheet <matchcodeio_gen-ai-search-test-100_results.ods>`
- the :download:`full JSON results<matchcodeio_gen-ai-search-test-100.json>`


Some future work include:

- Dealing with common files and common code fragments that are not copied code. These are
  essentially false positives. We could exclude them from indexing, filter then out of match
  results or apply a traditional IR ranking of results such as with tf/idf or BM25.

- Execute additional tuning of search results quality by adjusting fragment lengths.

- Extend index-time matching to approximate matching.
