import atexit
import tempfile
import time
import unittest
from pathlib import Path

from biocommons.eutils._internal.sqlitecache import SQLiteCache


class TestSQLiteCacheBase(unittest.TestCase):
    def setUp(self):
        _, self._fn = tempfile.mkstemp(suffix=".db")

        atexit.register(lambda: Path(self._fn).unlink())

        self.cache = SQLiteCache(self._fn)


class TestSQLiteCacheAttrLookup(TestSQLiteCacheBase):
    def test_str_str(self):
        k, v = "key1", "text"
        self.cache[k] = v
        assert v == self.cache[k]

    def test_str_int(self):
        k, v = "key2", 2
        self.cache[k] = v
        assert v == self.cache[k]

    def test_int_str(self):
        k, v = 3, "val4"
        self.cache[k] = v
        assert v == self.cache[k]

    def test_int_int(self):
        k, v = 5, 6
        self.cache[k] = v
        assert v == self.cache[k]

    def test_int_none(self):
        k, v = 7, None
        self.cache[k] = v
        assert v == self.cache[k]

    def test_none_int(self):
        k, v = None, 8
        self.cache[k] = v
        assert v == self.cache[k]


class TestSQLiteCacheDir(TestSQLiteCacheBase):
    def setUp(self):
        super().setUp()
        self.cache["a"] = "a"
        self.cache["b"] = "b"
        self.cache["b"] = "b2"
        self.cache["c"] = "c"

    def test_dir(self):
        assert {"a", "b", "c"} == set(dir(self.cache))

    def test_in(self):
        assert "a" in self.cache
        assert "b" in self.cache
        assert "c" in self.cache


class TestSQLiteCacheExpire(TestSQLiteCacheBase):
    def test_expire(self):
        self.cache["a"] = "a"
        self.cache["b"] = "b"
        time.sleep(5)
        self.cache["b"] = "b2"
        self.cache["c"] = "c"

        assert {"a", "b", "c"} == set(dir(self.cache))
        self.cache.expire(3)
        # b was updated and should be younger than 3 seconds old
        assert {"b", "c"} == set(dir(self.cache))


if __name__ == "__main__":
    unittest.main()
