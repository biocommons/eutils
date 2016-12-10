====================================================
eutils -- a simplified interface to NCBI E-Utilities
====================================================

eutils is a Python package to simplify searching, fetching, and
parsing records from NCBI using their E-utilities_ interface.

STATUS: This code is alpha. There are no known bugs, but the code
supports only a limited subset of E-Utilities replies.  PubMed, Gene,
RefSeq (nucleotide), and dbSNP data are well-represented; others are
not represented at all.

|pypi_badge| |build_status| `Source`_


Features
--------
* simple Pythonic interface for searching and fetching
* automatic query rate throttling per NCBI guidelines
* optional sqlite-based caching of compressed replies
* "façades" that facilitate access to essential attributes in replies



A Quick Example
---------------

::

  $ pip install eutils
  $ ipython

  >>> import eutils.client
  
  # Initialize a client. This client handles all caching and query
  # throttling
  >>> ec = eutils.client.Client()

  # search for tumor necrosis factor genes
  # any valid NCBI query may be used
  >>> esr = ec.esearch(db='gene',term='tumor necrosis factor')
  
  # fetch one of those (gene id 7157 is human TNF)
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
  #>>> [p.acv for p in eg.references[0].products][:3]
  #['NM_001126112.2', 'NM_001276761.1', 'NM_000546.5'] 

  # As a sample, grab the first product defined on this reference (order is arbitrary)
  >>> mrna = eg.references[0].products[0]
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

  # and the mrna has a product, the resulting protein:
  >>> str(mrna.products[0])
  'GeneCommentary(acv=NP_001119584.1,type=peptide,heading=Reference,label=isoform a)'



Important Notes
---------------

* **You are encouraged to** `browse issues
  <https://github.com/biocommons/eutils/issues>`_. Please report any
  issues you find.
* **Use a pip package specification to ensure stay within minor
  releases for API stability.** For example, ``eutils >=0.1,<0.2``.


Developing and Contributing
---------------------------

Contributions of bug reports, code patches, and documentation are
welcome!

Development occurs in the default branch. Please work in feature
branches or bookmarks from the default branch. Feature branches should
be named for the eutils issue they fix, as in
`121-update-xml-facades`.  When merging, use a commit message like
"closes #121: update xml facades to new-style interface". ("closes #n"
is recognized automatically and closes the ticket upon pushing.)

The included Makefile automates many tasks.  In particular, `make
develop` prepares a development environment and `make test` runs
unittests. (Please run tests before committing!)

Again, thanks for your contributions.


.. _E-utilities: http://www.ncbi.nlm.nih.gov/books/NBK25499/
.. _source: https://bitbucket.org/biocommons/eutis/

.. |pypi_badge| image:: https://badge.fury.io/py/eutils.png
  :target: https://pypi.python.org/pypi?name=eutils
  :align: middle

.. |build_status| image:: https://travis-ci.org/biocommons/eutils.svg?branch=master
  :target: https://travis-ci.org/biocommons/eutils
  :align: middle

