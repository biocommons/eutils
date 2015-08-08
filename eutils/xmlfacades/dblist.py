"""Provides support for parsing NCBI einfo queries as described here:

http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EInfo

Unfortunately, the reply from this endpoint is has two very different
modes: if called without an argument, it returns a list of databases;
if called with a single db= argument, it returns details about the
database.  That means that the client interface is necessarily very
different.

TODO: Implement classes for each and return appropriate class based on
reply.

"""

import eutils.xmlfacades.base


class DbList(eutils.xmlfacades.base.Base):

    _root_tag = 'DbList'

    @property
    def databases(self):
        return sorted(self._xml_elem.xpath('DbName/text()'))
