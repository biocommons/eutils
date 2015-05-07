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
        gc_xr = doc.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary')[0]
        gc = EntrezgeneSet(gc_xr)

if __name__ == '__main__':
    unittest.main()
