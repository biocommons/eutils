====================================================
eutils -- a simplified interface to NCBI E-Utilities
====================================================

eutils is a Python package dedicated to searching and fetching records
from NCBI using their E-Utilities interface.

A Quick Example
===============

::

  import eutils
  client = eutils.Client(email = 'your@emailaddress.com')
  pmr = client.pubmed.fetch(555)
  for pmr in client.pubmed.search('Hart RK [AU]'):
      print('{pmr.author1} wrote {pmr.title} in {pmr.year}'.format(pmr=pmr))

http://www.ncbi.nlm.nih.gov/books/NBK25499/


Installation and quick start
============================

