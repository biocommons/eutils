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

from eutils.exceptions import EutilsError
import eutils.xmlfacades.base
import eutils.xmlfacades.einforesult
import eutils.xmlfacades.dbinfo
import eutils.xmlfacades.dblist


class EInfoResult(eutils.xmlfacades.base.Base):

    _root_tag = 'eInfoResult'

    @property
    def type(self):
        "return 'dblist' or 'dbinfo' corresponding to the two major kinds of EInfoResult replies"
        childtag = self._xml_elem[0].tag
        if childtag == 'DbInfo':
            return 'dbinfo'
        elif childtag == 'DbList':
            return 'dblist'
        raise RuntimeError("Shouldn't be here; EInfoResult contains neither a DbList nor a DbInfo")

    @property
    def dbinfo(self):
        return eutils.xmlfacades.dbinfo.DbInfo(self._child('DbInfo'))

    @property
    def dblist(self):
        return eutils.xmlfacades.dblist.DbList(self._child('DbList'))

    # Internal Methods
    def _child(self, tag):
        n = self._xml_elem[0]
        if n.tag == tag:
            return n
        raise EutilsError("EInfoResult does not contain a " + tag + " child node")


if __name__ == "__main__":
    import gzip
    import os
    import lxml.etree as le
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')

    dir_path = os.path.join(data_dir, 'einfo.fcgi?db=protein&retmode=xml.xml.gz')
    dlr_path = os.path.join(data_dir, 'einfo.fcgi?retmode=xml.xml.gz')

    eiinfo = eutils.xmlfacades.einforesult.EInfoResult(le.XML(gzip.open(dir_path).read()))
    eilist = eutils.xmlfacades.einforesult.EInfoResult(le.XML(gzip.open(dlr_path).read()))

    dbinfo = eiinfo.dbinfo
    dblist = eilist.dblist
