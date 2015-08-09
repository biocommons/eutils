import os

import lxml.etree as le

from eutils.exceptions import *
from eutils.queryservice import QueryService
from eutils.xmlfacades.dbsnp import ExchangeSet
from eutils.xmlfacades.einforesult import EInfoResult
from eutils.xmlfacades.esearchresult import ESearchResult
from eutils.xmlfacades.gbset import GBSet
#from eutils.xmlfacades.gene import Gene
from eutils.xmlfacades.pubmedarticleset import PubmedArticleSet

# TODO: eutils-127: cache creation fails if ~/.cache doesn't already exist
default_cache_path = os.path.join(os.path.expanduser('~'), '.cache', 'eutils-cache.db')


class Client(object):
    def __init__(self, cache_path=default_cache_path, ):
        self._qs = QueryService(cache_path=cache_path)
        self.databases = self.einfo().dblist.databases

    def einfo(self, db=None):
        """query the einfo endpoint

        :param db: string (optional)
        :rtype: EInfo or EInfoDB object

        If db is None, the reply is a list of databases, which is returned
        in an EInfo object (which has a databases() method).

        If db is not None, the reply is information about the specified
        database, which is returned in an EInfoDB object.  (Version 2.0
        data is automatically requested.)
        """

        if db is None:
            return EInfoResult(self._qs.einfo()).dblist
        return EInfoResult(self._qs.einfo({'db': db, 'version': '2.0'})).dbinfo

    def esearch(self, db, term):
        """query the esearch endpoint
        """
        return ESearchResult(self._qs.esearch({'db': db, 'term': term}))

    def efetch(self, db, id):
        """query the efetch endpoint
        """
        db = db.lower()
        xml = self._qs.efetch({'db': db, 'id': str(id)})
        doc = le.parse(xml).getroot()
        if db in ['gene']:
            return Gene(doc)
        if db in ['nuccore']:
            # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see gbset.py)
            return GBSet(doc)
        if db in ['pubmed']:
            return iter(PubmedArticleSet(doc)).next()
        if db in ['snp']:
            return ExchangeSet(xml)
        raise EutilsError('database {db} is not currently supported by eutils'.format(db=db))
