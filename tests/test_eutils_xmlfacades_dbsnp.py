import os
import unittest

import eutils.xmlfacades.dbsnp

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_dbsnp_ExchangeSet(unittest.TestCase):
    def setUp(self):
        path = os.path.join(data_dir,'efetch.fcgi?db=snp&id=2031,14181&retmode=xml.xml')
        xml = open(path).read()
        self.es = eutils.xmlfacades.dbsnp.ExchangeSet(xml)

    def test_two_snps(self):
        assert len(self.es) == 2

if __name__ == '__main__':
    unittest.main()
