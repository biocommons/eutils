
Introduction
@@@@@@@@@@@@

eutils is a Python package to simplify searching, fetching, and
parsing records from NCBI using their E-utilities_ interface.

STATUS: This code is alpha. There are no known bugs, but the code supports
only a limited subset of E-Utilities replies.

|pypi_badge| |build_status| `Source`_


Features
########

* simple Pythonic interface for searching and fetching
* automatic query rate throttling per NCBI guidelines
* optional sqlite-based caching of compressed replies
* "façades" that facilitate access to essential attributes in XML replies


Important Notes
###############

* **You are encouraged to** `browse issues
  <https://github.com/biocommons/eutils/issues>`_. Please report any
  issues you find.
* **Use a pip package specification to ensure stay within minor
  releases for API stability.** For example, ``eutils >=0.1,<0.2``.




.. _E-utilities: http://www.ncbi.nlm.nih.gov/books/NBK25499/
.. _source: https://bitbucket.org/biocommons/eutis/

.. |pypi_badge| image:: https://badge.fury.io/py/eutils.png
  :target: https://pypi.python.org/pypi?name=eutils
  :align: middle

.. |build_status| image:: https://drone.io/bitbucket.org/biocommons/eutils/status.png
  :target: https://drone.io/bitbucket.org/biocommons/eutils
  :align: middle 
