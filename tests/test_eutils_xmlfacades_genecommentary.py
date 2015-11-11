import gzip
import os
import unittest

import lxml.etree

from eutils.xmlfacades.genecommentary import GeneCommentary

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_entrezgeneset(unittest.TestCase):
    def test_basic(self):
        path = os.path.join(data_dir,'entrezgeneset.xml.gz')
        doc = lxml.etree.parse(path).getroot()

        gc_xr = doc.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary')[0]
        gc = (gc_xr)

if __name__ == '__main__':
    unittest.main()
