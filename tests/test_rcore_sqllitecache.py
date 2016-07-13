import atexit
import collections
import os
import tempfile
import time
import unittest

from eutils.sqlitecache import SQLiteCache


class Test_SQLiteCacheBase(unittest.TestCase):

    def setUp(self):
        _,self._fn = tempfile.mkstemp(suffix='.db')
        
        atexit.register(lambda: os.remove(self._fn))

        self.cache = SQLiteCache(self._fn)



class Test_SQLiteCache_AttrLookup(Test_SQLiteCacheBase):

    def test_str_str(self):
        k,v = 'key1','text'
        self.cache[k] = v
        assert v == self.cache[k]
    
    def test_str_int(self):
        k,v = 'key2',2
        self.cache[k] = v
        assert v == self.cache[k]
    
    def test_int_str(self):
        k,v = 3,'val4'
        self.cache[k] = v
        assert v == self.cache[k]
    
    def test_int_int(self):
        k,v = 5,6
        self.cache[k] = v
        assert v == self.cache[k]
    
    def test_int_None(self):
        k,v = 7,None
        self.cache[k] = v
        assert v == self.cache[k]
    
    def test_None_int(self):
        k,v = None,8
        self.cache[k] = v
        assert v == self.cache[k]


class Test_SQLiteCache_Dir(Test_SQLiteCacheBase):

    def setUp(self):
        super(Test_SQLiteCache_Dir,self).setUp()
        self.cache['a'] = 'a'
        self.cache['b'] = 'b'
        self.cache['b'] = 'b2'
        self.cache['c'] = 'c'

    def test_dir(self):
        assert set(['a','b','c']) == set(dir(self.cache))
        
    def test_in(self):
        assert 'a' in self.cache
        assert 'b' in self.cache
        assert 'c' in self.cache


class Test_SQLiteCache_Expire(Test_SQLiteCacheBase):
    
    def test_expire(self):
        self.cache['a'] = 'a'
        self.cache['b'] = 'b'
        time.sleep(5)
        self.cache['b'] = 'b2'
        self.cache['c'] = 'c'
        
        assert set(['a','b','c']) == set(dir(self.cache))
        self.cache.expire(3)
        # b was updated and should be younger than 3 seconds old
        assert set(['b','c']) == set(dir(self.cache))
        

if __name__ == '__main__':
    unittest.main()
