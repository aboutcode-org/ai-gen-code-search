=========================================
  AI-Generated Code Search 
=========================================

``Search, detect, and identify AI-generated code.``

The AI-Generated Code Search project provides open source tools to find code that may have been
generated using LLMs and GPT tools.

Generative AI engines and Large Language Models (LLMs) are emerging as viable tools for software
developers to automate writing code. These engines and LLMs are trained on publicly available, free
and open source (FOSS) code.

AI-generated code can inherit the license and vulnerabilities of the FOSS code used for its
training. It is essential and urgent to identify AI-generated source code, as it threatens the
foundation of open source development and software development and raises major ethical, legal and
security questions.

Based on the AbouCode track record of creating industry-leading FOSS code origin analysis tools for
license and security, this project delivers a new approach to identify and detect if AI-generated
code is derived from existing FOSS with a new code fragments approximate similarity search.

We believe that AI-generated code identification is essential to ensure responsible use of that code
while enjoying the productivity gains from Generative AI for code. There is a massive potential for
misuse, malignant or illegal use of such code, and identifying AI-generated code will enable safer,
efficient and responsible use of GenAI to help build better software for the next generation
internet, faster and more efficiently.


Problem
-------------


FOSS is the foundation of all modern software. It is imperative to know the origin of reused FOSS
code and its vulnerabilities and licenses, especially for software supply chain security and
cybersecurity regulations, like SBOM mandates and Europe's upcoming CRA.

This applies to AI-generated code derived from FOSS code. The problem is so acute that several large
companies have issued policies prohibiting their programmers from using AI code generation tools.

Identifying AI-generated code requires matching using a large index of FOSS code. Scale is a
significant problem because incumbents need ever larger code indexes for accurate results, leading
to slower search queries and wasteful energy infrastructures.


Existing approaches identify code fragments only exactly and cannot work with AI-generated code as
each generation may yield different code, resulting in false negatives and false positives. All of
this results in serious concerns for organizations to use AI-generated code.


Goals
------------

This project goal is to deliver a reusable open source library and the indexing code to create an
open dataset to identify if source code is AI-generated and report which FOSS project it derives
from.

The intent is that AI-Generated Code Search will enhance trust for users searching for code on the
internet. This project aims to provide information and validation on the derivative open source
origin of AI-generated code to identify its vulnerabilities and licenses to mitigate any software
supply chain integrity or security risks associated with using AI-generated code.

We hope that this solution will increase users' trust of using both AI-generated code found on the
web and code created by a Generative AI engine or LLM.


Solution
---------

We need to provide quality and trustworthy approximate code fragments matching on smaller indexes to
accommodate the variety of AI-generated code and the growing volume of open source code used to
train the backing LLMs.

The ambition of this project is to provide a new approach to code matching with locality-sensitive
hashing (LSH) using random projections tunable for precision and recall, and avoid an ever
increasing code index size. This will make it practical for users to identify AI-generated code at
scale.

Providing a practical solution to discover AI-generated code fragments will improve the
trustworthiness of both AI-generated and non-generated code - and open source code in particular -
by reporting its AI-generated status and ultimate FOSS origin.


This project will enable trustworthy, safer and efficient usage of LLM-based code generation with
this critical knowledge, improving overall programmer productivity and adoption of responsible AI-
code generation tools.


Approach and Design
-----------------------

Existing code matching tools only match fragments exactly with low recall results, because exact
matching requires indexing the largest possible number of fragments to avoid false negative matches,
and this volume leads to more false positives. Exact matching does not work for AI-generated code
where each generation may have small variations given the same input prompt.

Our approach for matching code fragments consists of these three elements:

1. A content-defined chunking algorithm to split code into fragments - an improved alternative to
the common winnowing.

2. The fingerprinting of code with a locality sensitive hashing (LSH) function for approximate
matching of fragments. This fingerprint scheme embeds multiple precision in a single bit string to
tune the search precision and organize the search in rounds of progressively increasing precision.

3. An indexing-time matching with each new fragment only added to the index if it is not matchable
in the index, avoiding large duplications of FOSS code.


Implementation
----------------------------

Existing code fragment search solutions are either closed data, expensive proprietary closed source
solutions, or use code indexes that are too big to share. None are designed or adapted to support
AI-generated code search. Because of their costs, none are practical or accessible for SMEs or
individuals because they are too expensive to acquire and operate.

This project integrates with the open AboutCode stack's existing extensive and open code analysis
capabilities to enable:

1. Holistic and comprehensive knowledge of software code origin, including AI-generated code

2. Confidence that the licensing and known vulnerabilities of the whole code is tracked and managed

3. Direct support for CRA compliance, and the implied mandate to track code origin and report
security issues for software code


These tools are designed to be used either:

- As the building blocks for a larger solution, or
- As an integrated solution with the open source AboutCode stack.


Roadmap
--------------

The high level plan for this project is to:

- Design and implement core fingerprinting and content-defined chunking algorithms
- Execute evaluation and tuning of these algorithms
- Package these algorithms in a reusable library
- Design and implement index storage data structures
- Implement efficient hamming distance fingerprint matching, e.g., the core search
- Create AI-generated code test dataset. Reuse existing dataset where relevant
- Create reference dataset for indexing (reusing PurlDB and SWH)
- Create indexing pipeline and REST API with index-time matching
- Implement search results ranking procedure
- Create searching pipeline and REST API
- Create search query client to search a whole codebase
- Execute at-scale evaluation and tuning campaigns of end-to-end solution
- Package and document library and whole solution for easy deployment and reuse
- Deploy public demo system
- Present at FOSDEM and webinars for community dissemination


This repository also contains a SameCode library. See README_samecode.rst for details.


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
