import gzip
import os
import unittest

import pytest

import lxml.etree

from eutils.exceptions import EutilsError
from eutils.xmlfacades.einforesult import EInfoResult

data_dir = os.path.realpath(os.path.realpath(os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_einforesult(unittest.TestCase):
    @staticmethod
    def _read_file(fn):
        path = os.path.join(data_dir, fn)
        return EInfoResult(lxml.etree.parse(path).getroot())

    def setUp(self):
        self.eilist = self._read_file('einfo.fcgi?retmode=xml.xml.gz')
        self.eiinfo = self._read_file('einfo.fcgi?db=protein&retmode=xml.xml.gz')

    def test_einforesult_success(self):
        "Ensure EInfoResult methods work for tests data"
        assert self.eiinfo.dbinfo
        assert self.eilist.dblist

    def test_einforesult_failures(self):
        "Ensure EInfoResult methods work for tests data"
        with pytest.raises(EutilsError):
            _ = self.eiinfo.dblist
        with pytest.raises(EutilsError):
            _ = self.eilist.dbinfo

    def test_dblist_success(self):
        "Ensure DbList methods work for tests data"
        dblist = self.eilist.dblist
        assert 'protein' in dblist.databases
        assert len(dblist.databases) == 49

    def test_dbinfo_success(self):
        "Ensure DbInfo methods work for tests data"
        dbinfo = self.eiinfo.dbinfo
        assert dbinfo.count == '220301636'
        assert dbinfo.dbbuild == 'Build150805-2101m.1'
        assert dbinfo.dbname == 'protein'
        assert dbinfo.description == 'Protein sequence record'
        assert dbinfo.lastupdate == '2015/08/06 17:49'
        assert dbinfo.menuname == 'Protein'
    
if __name__ == '__main__':
    unittest.main()
