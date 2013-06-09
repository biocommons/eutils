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


Installation and quick start
============================

*The following instructions create a new virtualenv and install eutils
into it in a Unix/Linux environment.  Most users will eventually prefer to
install eutils into a separate environment or in the system path (as
root).*

::

  wget -nd https://raw.github.com/pypa/virtualenv/master/virtualenv.py
  python virtualenv.py --distribute ~/virtualenvs/eutils
  source ~/virtualenvs/eutils/bin/activate
  pip install eutils


