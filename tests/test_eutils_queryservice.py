from __future__ import absolute_import, unicode_literals

import unittest
import six
from lxml import etree

import eutils.client as ec

'''Performs a query using every form of eutils fcgi that this python 
library should support.

"If you liked it, then you shoulda put a test on it." --Beyonce'''


# helper function for elink test.
def parse_related_pmids_result(xmlstr):
    outd = {}
    dom = etree.fromstring(xmlstr)
    for linkset in dom.findall('LinkSet/LinkSetDb'):
        heading = linkset.find('LinkName').text.split('_')[-1]
        outd[heading] = []
        for Id in linkset.findall('Link/Id'):
            outd[heading].append(Id.text)
    return outd


def assert_in_xml(xml, item):
    if six.PY3 and type(xml) == six.binary_type:
        xml = xml.decode()
    assert item in xml

class TestEutilsQueries(unittest.TestCase):

    def setUp(self):
        self.qs = ec.QueryService()

    def tearDown(self):
        pass

    def test_efetch(self):
        '''Testing efetch.fcgi by looking up a known pubmed article.'''

        pmid = 1234567
        result = self.qs.efetch(args={'db': 'pubmed', 'id': pmid})
        assert_in_xml(result, str(pmid))

    def test_esearch(self):
        '''Testing esearch.fcgi by searching medgen db for concepts related to OCRL gene.'''
        # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=medgen&term=OCRL
        result = self.qs.esearch( { 'db': 'medgen', 'term': 'OCRL' } )

        # eSearchResult should contain something like this:
        #<IdList><Id>763754</Id><Id>336867</Id><Id>336322</Id><Id>168056</Id><Id>18145</Id></IdList>
        assert_in_xml(result, 'IdList')

    def test_elink(self):
        '''Testing elink.fcgi by looking up related pmids in pubmed.''' 
        #   Expected response should contain the following information:
            
        #    * pubmed    (all related links)
        #    * citedin   (papers that cited this paper)
        #    * five      (the "five" that pubmed displays as the top related results)
        #    * reviews   (review papers that cite this paper)
        #    * combined  (?)

        expected_keys = ['pubmed', 'citedin', 'five', 'reviews', 'combined']
        xmlstr = self.qs.elink( { 'dbfrom': 'pubmed', 'id': 1234567, 'cmd': 'neighbor' } )
 
        resd = parse_related_pmids_result(xmlstr)
        assert 'pubmed' in resd.keys()

    def test_esummary(self):
        '''Testing esummary.fcgi by looking up a known medgen concept'''

        # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=medgen&id=336867
        result = self.qs.esummary({ 'db': 'medgen', 'id': 336867 })
        assert_in_xml(result, 'ConceptId')

