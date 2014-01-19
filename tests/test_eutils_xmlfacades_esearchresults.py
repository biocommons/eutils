import os
import unittest

from eutils.xmlfacades.esearchresults import ESearchResults

tests_dir = os.path.dirname(__file__)
data_dir = os.path.join(tests_dir,'data')

class Test_exe_ESearchResults(unittest.TestCase):
    
    def setUp(self):
        xml = open(os.path.join(data_dir,'esearchresults-1.xml')).read()
        self.esr = ESearchResults(xml)

    def test_count(self):
        self.assertEqual( self.esr.count, 3 )
        
    def test_retmax(self):
        self.assertEqual( self.esr.retmax, 3 )
        
    def test_retstart(self):
        self.assertEqual( self.esr.retstart, 0 )
        
    def test_webenv(self):
        self.assertTrue( self.esr.webenv.startswith('NCID_')  )
        
    def test_ids(self):
        self.assertTrue( isinstance(self.esr.ids,list) )
        self.assertEqual( len(self.esr.ids), self.esr.count )
        self.assertEqual( sorted(self.esr.ids), sorted([19209718, 11108480, 6067859]) )
