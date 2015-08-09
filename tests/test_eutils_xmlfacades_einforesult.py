import gzip
import os
import unittest

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
        self.assertTrue(self.eiinfo.dbinfo)
        self.assertTrue(self.eilist.dblist)

    def test_einforesult_failures(self):
        "Ensure EInfoResult methods work for tests data"
        with self.assertRaises(EutilsError):
            _ = self.eiinfo.dblist
        with self.assertRaises(EutilsError):
            _ = self.eilist.dbinfo

    def test_dblist_success(self):
        "Ensure DbList methods work for tests data"
        dblist = self.eilist.dblist
        self.assertIn('protein', dblist.databases)
        self.assertEqual(49, len(dblist.databases))

    def test_dbinfo_success(self):
        "Ensure DbInfo methods work for tests data"
        dbinfo = self.eiinfo.dbinfo
        self.assertEqual('220301636', dbinfo.count)
        self.assertEqual('Build150805-2101m.1', dbinfo.dbbuild)
        self.assertEqual('protein', dbinfo.dbname)
        self.assertEqual('Protein sequence record', dbinfo.description)
        self.assertEqual('2015/08/06 17:49', dbinfo.lastupdate)
        self.assertEqual('Protein', dbinfo.menuname)
    
if __name__ == '__main__':
    unittest.main()
