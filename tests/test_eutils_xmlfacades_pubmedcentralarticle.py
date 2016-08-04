import gzip
import os
import unittest

import lxml.etree as le

from eutils.xmlfacades.pubmedcentralarticle import PubmedCentralArticle
from eutils.xmlfacades.pubmedcentralarticleset import PubmedCentralArticleSet

data_dir = os.path.realpath(os.path.realpath( os.path.join(__file__,'../data')))

class Test_eutils_xmlfacades_PubmedCentralArticle(unittest.TestCase):
    @staticmethod
    def _read_article_xml(relpath):
        path = os.path.join(data_dir,relpath)
        pas = PubmedCentralArticleSet(le.parse(path).getroot())
        pa = next(iter(pas))
        return pa

    def test_PMC3299399(self):
        pma = self._read_article_xml('efetch.fcgi?db=pmc&id=3299399&rettype=xml.xml')
        assert pma.pmc == '3299399'
        assert pma.pmid == '22416237'
        assert pma.doi == '10.3389/fpsyt.2012.00018'
        assert pma.title == 'The Effects of Psychosis Risk Variants on Brain Connectivity: A Review'
        assert 'It is characterized by hallucinations and delusions, reduced emotion and cognitive impairment' in pma.body_text

    def test___str__(self):
        'Ensure xmlfacade Base object safely converts to string.'
        # Although I'm agnostic about what the string representation should be, this is the current one
        pmca = self._read_article_xml('efetch.fcgi?db=pmc&id=3299399&rettype=xml.xml')
        assert 'PubmedCentralArticle(pmc=3299399;pmid=22416237;doi=10.3389/fpsyt.2012.00018;The Effects of Psychosis Risk Variants on Brain Connectivity: A Review)' in str(pmca)

if __name__ == '__main__':
    unittest.main()
