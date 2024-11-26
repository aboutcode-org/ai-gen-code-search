.. _installation:

Installation
============

Welcome to **SameCode** installation guide. This guide describes how to install
SameCode. Please read and follow the instructions carefully to ensure
your installation is functional and operational.

The **preferred SameCode installation** is to install with pip. Or to clone and work from git.

Install with pip
^^^^^^^^^^^^^^^^^^^^^^^

    pip install samecode


Or clone and configure
^^^^^^^^^^^^^^^^^^^^^^^

**Clone the git** `SameCode repo <https://github.com/aboutcode-org/ai-gen-code-search>`_,
and configure your environment::

    git clone https://github.com/aboutcode-org/ai-gen-code-search.git && cd ai-gen-code-search
    make dev


Run tests
^^^^^^^^^^^

**Run the tests suite**::

    make test

At this point, the SameCode app should be available for your usage.


Supported Platforms
^^^^^^^^^^^^^^^^^^^

**SameCode** has been tested and is supported on the following operating systems:

    #. **Debian-based** Linux distributions

.. note::
    **macOS**, **Windows**, and other **Linux** distributions are likely working too, but have
    not been tested.

.. warning::
     On **Windows** SameCode can likely **only** run with WSL2.

