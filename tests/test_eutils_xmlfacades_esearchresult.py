import gzip
import os
import unittest

from eutils.xmlfacades.esearchresult import ESearchResult

tests_dir = os.path.dirname(__file__)
data_dir = os.path.join(tests_dir,'data')

class Test_ESearchResult(unittest.TestCase):
    
    def setUp(self):
        path = os.path.join(data_dir,'esearch.fcgi?term=hart%20rk[author].xml.gz')
        xml = gzip.open(path).read()
        self.expected_ids = [6067859, 11108480, 19209718, 24667040, 25273102]
        self.esr = ESearchResult(xml)

    def test_count(self):
        assert self.esr.count == 5 
        
    def test_retmax(self):
        assert self.esr.retmax == 5 
        
    def test_retstart(self):
        assert self.esr.retstart == 0 
        
    def test_webenv(self):
        assert self.esr.webenv is None
        
    def test_ids(self):
        assert isinstance(self.esr.ids,list)
        assert len(self.expected_ids) == self.esr.count
        assert sorted(self.expected_ids) == sorted(self.esr.ids)
