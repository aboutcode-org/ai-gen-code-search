.. _installation:

Installation
============

This is an installation guide to evaluate the AI-generated code search features of AboutCode.

The search for AI-generated code needs to have these sub-systems deployed and installed:

- PurlDB: a database of software package metadata, and an index of their files and file
  fingerprints.

- MatchCode: a backend code matching service that has direct access to the PurlDB database and
  executes a rich pipeline of code matching steps, from exact package, file tree or file, to
  approximate code tree, file and code fragments, including possibly generated and refactored code
  fragments.

- ScanCode.io: a frontend code scanning service that receives the codebase to analyse as inputs,
  then scans and computes fingerprints to send to the MatchCode backend for matching, before
  presenting consolidated matching results.

This guide describes and provide pointers on how to install each of the three components.

Alternatively, we maintain a publicly accessible, fully deployed evaluation system with each of
these three components. Please reach out to hello@aboutcode.org to gain access to this environment.


Install the backend: PurlDB and MatchCode.io
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow instructions to get started at:
https://aboutcode.readthedocs.io/projects/PURLdb/en/latest/getting-started/index.html

Then follow installation instructions at:

- https://aboutcode.readthedocs.io/projects/PURLdb/en/latest/getting-started/install.html
- https://aboutcode.readthedocs.io/projects/PURLdb/en/latest/how-to-guides/installation.html

This will also install MatchCode.io.


Install the frontend: ScanCode.io
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow insructions at:
https://scancodeio.readthedocs.io/en/latest/installation.html



Configure ScanCode.io for PurlDB access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Follow insructions at:
https://scancodeio.readthedocs.io/en/latest/application-settings.html#purldb



Run a simple test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See instructions at:
https://aboutcode.readthedocs.io/projects/PURLdb/en/latest/how-to-guides/matchcode.html


You can also index the package ``pkg:npm/inherits@2.0.3`` to support the step-by-step
end to end tutorial :ref:`e2e-ai-gen-code`.


See also https://zenodo.org/records/15449709 for a larger dataset of popular package PURLs.
