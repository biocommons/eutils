"""simple key-value cache with transparent payload compression and expiration

Taken from http://bitbucket.org/reece/rcore/
"""

import cPickle
import logging
import os
import sqlite3
import zlib


def key_to(o):
    return cPickle.dumps(o)
def key_from(po):
    return cPickle.loads(po)
def val_to(o,compress):
    po = cPickle.dumps(o)
    return zlib.compress(po) if compress else pop
def val_from(po,compress):
    return cPickle.loads(zlib.decompress(po) if compress else po)


class SQLiteCache(object):

    ############################################################################
    ## Exposed methods
    def __init__(self,db_path,compress_values=True):
        self.compress_values = compress_values
        self._con = None
        self._logger = logging.getLogger(__name__)
        self._connect(db_path)

    def expire(self,age):
        cur = self._execute("DELETE FROM cache WHERE strftime('%s','now') - created > ?",[age])
        return cur.rowcount
        
    ############################################################################
    ## Special Python methods
    def __unicode__(self):
        return 'SQLiteCache(db_path={self._db_path},compress_values={self.compress_values})'.format(self=self)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __dir__(self):
        self._logger.debug('__dir__()')
        return [key_from(row[0])
                for row in self._execute('SELECT key FROM cache',[])]

    def __getitem__(self,key):
        self._logger.debug('__getitem__({key})'.format(key=key))
        cur = self._execute('SELECT value,value_compressed FROM cache WHERE key = ?',[key_to(key)])
        row = cur.fetchone()
        if row is None:
            raise KeyError(key)
        return val_from(*row)

    def __setitem__(self,key,value):
        db_val = val_to(value,self.compress_values)
        self._logger.debug('__setitem__({key},({vlen} bytes))'.format(key=key,vlen=len(db_val)))
        self._execute('INSERT OR REPLACE INTO cache (key,value_compressed,value) VALUES (?,?,?)',
                      [key_to(key), self.compress_values, db_val])

    def __delitem__(self,key):
        self._logger.debug('__delitem__({key})'.format(key=key))
        cur = self._execute('DELETE FROM cache WHERE key = ?',[key_to(key)])
        if cur.rowcount == 0:
            raise KeyError(key)

    def __contains__(self,key):
        self._logger.debug('__contains__({key})'.format(key=key))
        return self._fetch1v('SELECT EXISTS(SELECT 1 FROM cache WHERE key=? LIMIT 1)',[key_to(key)])


    ############################################################################
    ## Internal functions

    def _connect(self,db_path):
        assert self._con is None, 'already connected'
        self._con = sqlite3.connect(db_path,isolation_level=None)
        self._con.text_factory = str
        self._db_path = db_path
        self._logger.info('opened '+db_path)
        sver = self._get_schema_version()
        self._logger.debug('schema version is '+str(sver))
        if sver is None:
            self._execute("CREATE TABLE cache (key BLOB PRIMARY KEY, created INTEGER DEFAULT (strftime('%s','now')), value_compressed BOOL, value BLOB)")
            self._execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            self._execute("INSERT INTO meta (key, value) VALUES (?,?)",['schema version',1])
            self._logger.debug('created tables')
        
    def _get_schema_version(self):
        if (u'meta',) not in self._execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            return None
        return self._fetch1v('SELECT value FROM meta WHERE key = ?', ['schema version'])

    def _execute(self,query,params=[]):
        cur = self._con.cursor()
        self._logger.debug('executing query <{query}> with params <{nvars} vars>'.format(
            query=query, nvars=len(params)))
        cur.execute(query,params)
        return cur

    def _fetch1v(self,query,params=[]):
        return self._execute(query,params).fetchone()[0]


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    c = SQLiteCache('/tmp/SQLiteCache-test.db')
