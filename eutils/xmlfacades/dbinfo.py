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



class DbInfo(eutils.xmlfacades.base.Base):

    _root_tag = 'DbInfo'

    @property
    def dbname(self):
        return self._xml_elem.findtext('DbName')

    @property
    def menuname(self):
        return self._xml_elem.findtext('MenuName')

    @property
    def description(self):
        return self._xml_elem.findtext('Description')

    @property
    def dbbuild(self):
        return self._xml_elem.findtext('DbBuild')

    @property
    def count(self):
        return self._xml_elem.findtext('Count')

    @property
    def lastupdate(self):
        return self._xml_elem.findtext('LastUpdate')
