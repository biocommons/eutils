import pprint,unittest

from locus.ncbi.pubmedarticle import PubMedArticle

class Test_LocusNCBIPubMedArticle(unittest.TestCase):
    def test_2(self):
        a = PubMedArticle(2)
        self.assertEquals(a.jrnl,'Biochem. Biophys. Res. Commun.')
        self.assertEquals(a.pii, '0006-291X(75)90482-9')
        self.assertIsNone(a.pmc)

    def test_17082447(self):
        a = PubMedArticle(17082447)
        self.assertEquals(a.jrnl,'Science')

    def test_20625499(self):
        a = PubMedArticle(20625499)
        self.assertEquals(a.doi,'10.1155/2010/597641')
        self.assertEquals(a.jrnl,'J. Biomed. Biotechnol.')
        self.assertEquals(a.pmc,'2896701')

    def test_20412080(self):
        a = PubMedArticle(20412080)
        self.assertEquals(a.author1_last_fm, 'Robinson PN')
        self.assertEquals(a.author1_lastfm, 'RobinsonPN')
        self.assertEquals(a.authors_str,'Robinson PN; Mundlos S')
        self.assertEquals(a.doi, '10.1111/j.1399-0004.2010.01436.x')
        self.assertEquals(a.jrnl,'Clin. Genet.')
        self.assertEquals(a.pages,'525-34')
        self.assertEquals(a.pii, 'CGE1436')
        self.assertEquals(a.title, 'The human phenotype ontology.')
        self.assertEquals(a.voliss,'77(6)')
        self.assertEquals(a.year,'2010')

    def test_21829395(self):
        a = PubMedArticle(21829395)
        self.assertEquals(a.jrnl,'PLoS Genet.')
        self.assertEquals(a.pii, 'PGENETICS-D-11-00469')
        self.assertEquals(a.pmc,'3150440')


if __name__ == '__main__':
    unittest.main()
