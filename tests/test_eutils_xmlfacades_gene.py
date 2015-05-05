import os,unittest

import eutils.xmlfacades.gene

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_gene_Gene(unittest.TestCase):
    def test_NEFL(self):
        xml = open(os.path.join(data_dir,'efetch.fcgi?retmode=xml&db=gene&id=4747.xml')).read()
        g = eutils.xmlfacades.gene.Gene(xml)
        self.assertEqual(g.description, 'neurofilament, light polypeptide')
        self.assertEqual(g.hgnc, 'NEFL')
        self.assertEqual(g.maploc, '8p21')
        self.assertTrue(g.summary.startswith('Neurofilaments are type IV intermediate filament'))

if __name__ == '__main__':
    unittest.main()
