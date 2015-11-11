import gzip
import os
import unittest

import lxml.etree as le

from eutils.xmlfacades.pubmedarticle import PubmedArticle
from eutils.xmlfacades.pubmedarticleset import PubmedArticleSet

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_PubmedArticle(unittest.TestCase):
    @staticmethod
    def _read_article_xml(relpath):
        path = os.path.join(data_dir,relpath)
        pas = PubmedArticleSet(le.parse(path).getroot())
        pa = next(iter(pas))
        return pa

    def test_20412080(self):
        pma = self._read_article_xml('efetch.fcgi?db=pubmed&id=20412080&rettype=xml.xml')

        self.assertTrue(pma.abstract.startswith('A standardized, controlled vocabulary allows phenotypic'))
        self.assertEqual(set(pma.authors), set(['Robinson PN', 'Mundlos S']))
        self.assertEqual(pma.doi, '10.1111/j.1399-0004.2010.01436.x')
        self.assertEqual(pma.issue, '6')
        self.assertEqual(pma.jrnl, 'Clin. Genet.')
        self.assertEqual(set(pma.mesh_headings),
                         set(['Algorithms',
                              'Computational Biology',
                              'Databases, Genetic',
                              'Gene Expression',
                              'Humans',
                              'Phenotype',
                              'Vocabulary, Controlled']))
        self.assertEqual(pma.pages, '525-34')
        self.assertEqual(pma.pii, 'CGE1436')
        self.assertIsNone(pma.pmc)
        self.assertEqual(pma.pmid, '20412080')
        self.assertEqual(pma.title, 'The human phenotype ontology.')
        self.assertEqual(pma.volume, '77')
        self.assertEqual(pma.year, '2010')

    def test_23121403(self):
        pma = self._read_article_xml('efetch.fcgi?db=pubmed&id=23121403&retmode=xml.xml')

        self.assertIn('ASPIRE Investigators', pma.authors)

    def test_22351513(self):
        pma = self._read_article_xml('efetch.fcgi?db=pubmed&id=22351513&retmode=xml.xml')

        self.assertIn('Mahmooduzzafar', pma.authors)

    def test___str__(self):
        'Ensure xmlfacade Base object safely converts to string.'
        pma = self._read_article_xml('efetch.fcgi?db=pubmed&id=20412080&rettype=xml.xml')
        self.assertIn('PubmedArticle(20412080', '%s' % pma)

if __name__ == '__main__':
    unittest.main()
