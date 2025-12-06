# biocommons.example

[![Release](https://img.shields.io/github/v/release/biocommons/python-package)](https://img.shields.io/github/v/release/biocommons/python-package)
[![Build status](https://img.shields.io/github/actions/workflow/status/biocommons/python-package/main.yml?branch=main)](https://github.com/biocommons/python-package/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/biocommons/python-package/branch/main/graph/badge.svg)](https://codecov.io/gh/biocommons/python-package)
[![Commit activity](https://img.shields.io/github/commit-activity/m/biocommons/python-package)](https://img.shields.io/github/commit-activity/m/biocommons/python-package)
[![License](https://img.shields.io/github/license/biocommons/python-package)](https://img.shields.io/github/license/biocommons/python-package)

Package Description

This project is a product of the [biocommons](https://biocommons.org/) community.

- **Github repository**: <https://github.com/biocommons/python-package/>
- **Documentation** <https://biocommons.github.io/python-package/>

## Python Package Installation

Install from PyPI with `pip install biocommons.example` or `uv pip install biocommons.example`, then try it:

    $ source venv/bin/activate

    $ python3 -m biocommons.example
    Marvin says:
    There's only one life-form as intelligent as me within thirty parsecs...

    $ marvin-quote
    Marvin says:
    You think you've got problems? What are you supposed to do if you...

    $ ipython
    >>> from biocommons.example import __version__, get_quote_from_marvin
    >>> __version__
    '0.1.dev8+gd5519a8.d20211123'
    >>> get_quote()
    "The first ten million years were the worst, ...


## Developer Setup

### Install Prerequisites

These tools are required to get started:

- [git](https://git-scm.com/): Version control system
- [GNU make](https://www.gnu.org/software/make/): Current mechanism for consistent invocation of developer tools.
- [uv](https://docs.astral.sh/uv/): An extremely fast Python package and project manager, written in Rust.

#### MacOS or Linux Systems

- [Install brew](https://brew.sh/)
- `brew install git make uv`

#### Linux (Debian-based systems)

You may also install using distribution packages:

    sudo apt install git make

Then install uv using the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

### One-time developer setup

Create a Python virtual environment, install dependencies, install pre-commit hooks, and install an editable package:

    make devready

### Development

**N.B.** Developers are strongly encouraged to use `make` to invoke tools to
ensure consistency with the CI/CD pipelines.  Type `make` to see a list of
supported targets.  A subset are listed here:

    » make
    🌟🌟 biocommons conventional make targets 🌟🌟

    Using these targets promots consistency between local development and ci/cd commands.

    usage: make [target ...]

    BASIC USAGE
    help                Display help message

    SETUP, INSTALLATION, PACKAGING
    devready            Prepare local dev env: Create virtual env, install the pre-commit hooks
    build               Build package
    publish             publish package to PyPI

    FORMATTING, TESTING, AND CODE QUALITY
    cqa                 Run code quality assessments
    test                Test the code with pytest

    DOCUMENTATION
    docs-serve          Build and serve the documentation
    docs-test           Test if documentation can be built without warnings or errors

    CLEANUP
    clean               Remove temporary and backup files
    cleaner             Remove files and directories that are easily rebuilt
    cleanest            Remove all files that can be rebuilt
    distclean           Remove untracked files and other detritus
