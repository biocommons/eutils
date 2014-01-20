import os,unittest

import eutils.xmlfacades.pubmed

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_pubmed_PubMedArticle(unittest.TestCase):
    def test_20412080(self):
        xml = open(os.path.join(data_dir,'efetch.fcgi?rettype=xml&db=pubmed&id=20412080.xml')).read()
        pma = eutils.xmlfacades.pubmed.PubMedArticle(xml)

        print(pma)

        self.assertTrue(pma.abstract.startswith('A standardized, controlled vocabulary allows phenotypic'))
        self.assertEqual(set(pma.authors), set(['Robinson PN', 'Mundlos S']))
        self.assertIsNone(pma.doi)
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
        self.assertIsNone(pma.pii)
        self.assertIsNone(pma.pmc)
        self.assertEqual(pma.pmid, '20412080')
        self.assertEqual(pma.title, 'The human phenotype ontology.')
        self.assertEqual(pma.volume, '77')
        self.assertEqual(pma.year, '2010')

        self.assertEqual(pma.as_dict(), {
                'abstract': 'A standardized, controlled vocabulary allows phenotypic information to be described in an unambiguous fashion in medical publications and databases. The Human Phenotype Ontology (HPO) is being developed in an effort to provide such a vocabulary. The use of an ontology to capture phenotypic information allows the use of computational algorithms that exploit semantic similarity between related phenotypic abnormalities to define phenotypic similarity metrics, which can be used to perform database searches for clinical diagnostics or as a basis for incorporating the human phenome into large-scale computational analysis of gene expression patterns and other cellular phenomena associated with human disease. The HPO is freely available at http://www.human-phenotype-ontology.org.',
                'authors': ['Robinson PN', 'Mundlos S'],
                'issue': '6',
                'jrnl': 'Clin. Genet.',
                'mesh_headings': ['Algorithms',
                                  'Computational Biology',
                                  'Databases, Genetic',
                                  'Gene Expression',
                                  'Humans',
                                  'Phenotype',
                                  'Vocabulary, Controlled'],
                'pages': '525-34',
                'pmid': '20412080',
                'title': 'The human phenotype ontology.',
                'volume': '77',
                'year': '2010'}
                         )


if __name__ == '__main__':
    unittest.main()
