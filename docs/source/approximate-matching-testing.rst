==================================================
Testing for approximate search
==================================================

The testing approach for approximate search consists in:

- validating the intrisinc attributes of our fingerprinting approach wrt. to measuring similarity
- aquiring test data to validate the end-to-end procedure
- running end-to-end tests for similarity search


We use these trest data:

- synthetic random data to validate the attributes of the fingerprint ability to detect similarity
- a public data set available on Zenodo [LLMZENODO]

The test data and scripts are stored in https://github.com/aboutcode-org/matchcode-tests/


Test report and status as of 2024-11-12:

The synthetic data tests perform according to expectations and observed results are close
to expected theoritical results. See the companiion spreadsheet halohash-distance-plots.ods
that plots content similarity buildup against the observed hamming distance computed between
fingerprints. The results are roughly a line and they match the expected according buildup of
similarity that would be expected.

The AI-Generated code tests consists of a code that is generated using OpenAI ChatGpl-3.5 and
ChatGPT-4. We selected a subset of the data set to make it practical to run in our project's
context. The data is self-described as::

    This dataset includes a collection of ten LeetCode programming problems used in the study
    "Analyzing the Dependability of Large Language Models for Code Clone Generation". At the top
    level, you will find a CSV file containing all the initial LeetCode data. Each subdirectory at
    this level represents a specific LeetCode problem. Within these subdirectories, you will find
    the original solutions, their behaviors, the input corpus, as well as folders dedicated to
    various temperatures, models, and code cloning tasks. Additionally, within the "repeated"
    folder, you will find the original LLM-generated snippets, the preprocessed snippets with the
    snippet behavior, and the results.

    This zipped directory encompasses the core scripts and results used in the "Characterizing Code
    Clones of LLMs" research. The common folder was used to run the whole pipeline, the various
    parts of the pipeline are each in a folder as well as the various data analysis scripts.

We built a test harness on top of this data to evaluate the end-to-end performance of our detection.
There are two key insights from these test runs:

1. Overall our approach is working in the simple cases
2. We need to tune carefully our choice of parameters. In particular, the choice of the ngrams
   length is critical and influence the false positive and false negative directly.
3. There is a class of AI-generated code "clones" that we are not able to detect correctly. These
   are duplicated code where the overall code flow are similar, but the variable names are different
   and there are different (or absent) code comment.

Because of this we need to design a new approach. The key to this new design will be to pre-process
code using token replacements. This is a technique developed in [GRUNE] where code is pre-processed
and code tokens are replaced by an abstract value. For instance an "if" instruction may be replaced
by a "C" for conditional; or an "index" variable or class name may be replaced by a "V" for
variable. This pre-processing takes place before actual chunking the content and fingerprinting, and
with it code that is essentially similar will be abstracted to its essence, ignoring naming styles
and preferences.


References
---------------

- [LLMZENODO] "Analyzing the Dependability of Large Language Models for Code Clone Generation"
  https://zenodo.org/records/11398703

- [GRUNE] "The software and text similarity tester SIM"
  https://www.dickgrune.com/Programs/similarity_tester/index.html
