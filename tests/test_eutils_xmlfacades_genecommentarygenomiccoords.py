import gzip
import os
import unittest

import lxml.etree

from eutils.xmlfacades.genecommentarygenomiccoords import GeneCommentaryGenomicCoords

data_dir = os.path.join(os.path.dirname(__file__), '..', 'tests', 'data')

class Test_eutils_xmlfacades_entrezgeneset(unittest.TestCase):

    def setUp(self):
        data_file = os.path.join(data_dir, 'entrezgeneset.xml.gz')
        self.egs_doc = lxml.etree.parse(gzip.open(data_file))

    def test_basic(self):
        gcgc_e = self.egs_doc.findall('.//Gene-commentary_genomic-coords')[0]
        gcgc = GeneCommentaryGenomicCoords(gcgc_e)
        assert gcgc.strand == 1
        assert gcgc.gi == 

if __name__ == '__main__':
    unittest.main()
