====================================================
eutils -- a simplified interface to NCBI E-Utilities
====================================================

eutils is a Python package to simplify searching, fetching, and
parsing records from NCBI using their E-utilities_ interface.

STATUS: This code is alpha. There are no known bugs, but the code supports
only a limited subset of E-Utilities replies.

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

  In [1]: import eutils.client
  
  In [2]: esr = ec.esearch(db='gene',term='tumor necrosis factor')
  
  In [3]: gb = ec.efetch(db='gene',id=esr.ids[0])
  
  In [4]: gb.locus, gb.maploc, gb.description, gb.type
  Out[4]: ('TP53', '17p13.1', 'tumor protein p53', 'protein-coding')

  In [5]: [ str(r) for r in gb.references ]
  Out[5]: 
  ['GeneCommentary(acv=NC_000017.10,type=genomic,heading=Reference GRCh37.p13 Primary Assembly,label=chromosome 17 reference GRCh37.p13 Primary Assembly)',
   'GeneCommentary(acv=NG_017013.2,type=genomic,heading=Reference assembly,label=RefSeqGene)',
   'GeneCommentary(acv=NC_018928.2,type=genomic,heading=Alternate CHM1_1.1,label=chromosome 17 alternate CHM1_1.1)',
   'GeneCommentary(acv=AC_000149.1,type=genomic,heading=Alternate HuRef,label=chromosome 17 alternate HuRef)']
  
  In [6]: gb.references[0].acv
  Out[6]: 'NC_000017.10'
  
  In [7]: gb.references[0].products[0].acv
  Out[7]: 'NM_001126112.2'
  
  In [8]: gb.references[0].products[0].genomic_coords.strand
  Out[8]: -1

  In [9]: gb.references[0].products[0].genomic_coords.intervals
  Out[9]: 
  [(7590694, 7590868),
   (7579838, 7579937),
   (7579699, 7579721),
   (7579311, 7579590),
   (7578370, 7578554),
   (7578176, 7578289),
   (7577498, 7577608),
   (7577018, 7577155),
   (7576852, 7576926),
   (7573926, 7574033),
   (7571719, 7573008)]
  


Important Notes
---------------

* **You are encouraged to** `browse issues
  <https://bitbucket.org/biocommons/eutils/issues>`_. Please report any
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
