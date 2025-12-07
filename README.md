# eutils -- simplified interface to NCBI E-Utilities

[![Release](https://img.shields.io/github/v/release/biocommons/eutils)](https://img.shields.io/github/v/release/biocommons/eutils)
[![Build status](https://img.shields.io/github/actions/workflow/status/biocommons/eutils/python-ci-cd.yml?branch=main)](https://github.com/biocommons/eutils/actions/workflows/python-ci-cd.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/biocommons/eutils/branch/main/graph/badge.svg)](https://codecov.io/gh/biocommons/eutils)
[![Commit activity](https://img.shields.io/github/commit-activity/m/biocommons/eutils)](https://img.shields.io/github/commit-activity/m/biocommons/eutils)
[![License](https://img.shields.io/github/license/biocommons/eutils)](https://img.shields.io/github/license/biocommons/eutils)

**eutils is a Python package to simplify searching, fetching, and parsing
records from NCBI using their
[E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25500/) interface**

## Features

* simple Pythonic interface for searching and fetching
* Support for [NCBI API keys](https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/), and rate throttling when no key is available
* optional sqlite-based caching of compressed replies
* "façades" that facilitate access to essential attributes in XML replies

- **Github repository**: <https://github.com/biocommons/eutils/>
- **Documentation** <https://eutils.readthedocs.io/en/stable/>

## Example Usage

    $ uv pip install eutils
    $ export NCBI_API_KEY=8d4b...
    $ ipython

    >>> import os
    >>> from biocommons.eutils import Client

    # Initialize a client. This client handles all caching and query
    # throttling.  For example:
    >>> ec = Client(api_key=os.environ.get("NCBI_API_KEY", None))

    # search for tumor necrosis factor genes
    # any valid NCBI query may be used
    >>> esr = ec.esearch(db='gene',term='tumor necrosis factor')

    # esearch returns a list of entity IDs associated with your search. preview some of them:
    >>> esr.ids[:5]
    [136114222, 136113226, 136112112, 136111930, 136111620]

    # fetch data for an ID (gene id 7157 is human TNF)
    >>> egs = ec.efetch(db='gene', id=7157)

    # One may fetch multiple genes at a time. These are returned as an
    # EntrezgeneSet. We'll grab the first (and only) child, which returns
    # an instance of the Entrezgene class.
    >>> eg = egs.entrezgenes[0]

    # Easily access some basic information about the gene
    >>> eg.hgnc, eg.maploc, eg.description, eg.type, eg.genus_species
    ('TP53', '17p13.1', 'tumor protein p53', 'protein-coding', 'Homo sapiens')

    # get a list of genomic references
    >>> sorted([(r.acv, r.label) for r in eg.references])
    [('NC_000017.11', 'Chromosome 17 Reference GRCh38...'),
    ('NC_018928.2', 'Chromosome 17 Alternate ...'),
    ('NG_017013.2', 'RefSeqGene')]

    # Get the first three products defined on GRCh38
    >>> [p.acv for p in eg.references[0].products][:3]
    ['NM_001126112.2', 'NM_001276761.1', 'NM_000546.5']

    # As a sample, grab the first product defined on this reference (order is arbitrary)
    >>> mrna = [i for i in eg.references[0].products if i.type == "mRNA"][0]
    >>> str(mrna)
    'GeneCommentary(acv=NM_001126112.2,type=mRNA,heading=Reference,label=transcript variant 2)'

    # mrna.genomic_coords provides access to the exon definitions on this reference
    >>> mrna.genomic_coords.gi, mrna.genomic_coords.strand
    ('568815581', -1)

    >>> mrna.genomic_coords.intervals
    [(7687376, 7687549), (7676520, 7676618), (7676381, 7676402),
    (7675993, 7676271), (7675052, 7675235), (7674858, 7674970),
    (7674180, 7674289), (7673700, 7673836), (7673534, 7673607),
    (7670608, 7670714), (7668401, 7669689)]

    # and if the mrna has a product, the resulting protein:
    >>> str(mrna.products[0])
    'GeneCommentary(acv=NP_001119584.1,type=peptide,heading=Reference,label=isoform a)'


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
