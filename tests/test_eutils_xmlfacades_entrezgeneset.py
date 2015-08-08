import gzip
import os
import unittest

import lxml.etree

from eutils.xmlfacades.entrezgeneset import EntrezgeneSet

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_entrezgeneset(unittest.TestCase):
    def test_basic(self):
        xml = gzip.open(os.path.join(data_dir,'entrezgeneset.xml.gz')).read()
        doc = lxml.etree.XML(xml)
        egs = EntrezgeneSet(doc)

if __name__ == '__main__':
    unittest.main()
