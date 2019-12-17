eutils -- a simplified interface to NCBI E-Utilities
====================================================

|pypi_badge| |build_status| |issues_badge| |contributors| |license| |docs| |changelog|

eutils is a Python package to simplify searching, fetching, and
parsing records from NCBI using their E-utilities_ interface.


News
----

* 0.5.0 was released on 2018-11-20. See `0.5 Change Log
  <https://eutils.readthedocs.io/en/stable/changelog/0.5.html>`_.



Features
--------
* simple Pythonic interface for searching and fetching
* automatic query rate throttling per NCBI guidelines
* optional sqlite-based caching of compressed replies
* "façades" that facilitate access to essential attributes in replies



A Quick Example
---------------

As of May 1, 2018, NCBI throttles requests based on whether a client
is registered. Unregistered clients are limited to 3 requests/second;
registered clients are granted 10 requests/second, and may request
more. See the `NCBI Announcement
<https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/>`_
for more information. 

The eutils package will automatically throttle requests according to
NCBI guidelines (3 or 10 requests/second without or with an API key,
respectively).

::

  $ pip install eutils
  $ ipython

  >>> from eutils import Client
  
  # Initialize a client. This client handles all caching and query
  # throttling.  For example:
  >>> ec = Client(api_key=os.environ.get("NCBI_API_KEY", None))

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
  releases for API stability.** For example, ``eutils >=0.6,<0.7``.


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


.. |build_status| image:: https://travis-ci.org/biocommons/eutils.svg?branch=master
  :target: https://travis-ci.org/biocommons/eutils

.. |changelog| image:: https://img.shields.io/badge/docs-changelog-green.svg
   :target: https://eutils.readthedocs.io/en/stable/changelog/

.. |contributors| image:: https://img.shields.io/github/contributors/biocommons/eutils.svg
  :target: https://github.com/biocommons/eutils

.. |docs| image:: https://img.shields.io/badge/docs-readthedocs-green.svg
   :target: http://eutils.readthedocs.io/

.. |issues_badge| image:: https://img.shields.io/github/issues/biocommons/eutils.png
  :target: https://github.com/biocommons/eutils/issues
  :align: middle

.. |license| image:: https://img.shields.io/github/license/biocommons/eutils.svg
  :target: https://github.com/biocommons/eutils/blob/master/LICENSE

.. |pypi_badge| image:: https://img.shields.io/pypi/v/eutils.svg
  :target: https://pypi.org/project/eutils/
