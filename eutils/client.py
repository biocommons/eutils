import os

from eutils.exceptions import *
from eutils.queryservice import QueryService
from eutils.xmlfacades.dbsnp import ExchangeSet
from eutils.xmlfacades.einfo import EInfo, EInfoDB
from eutils.xmlfacades.esearchresults import ESearchResults
from eutils.xmlfacades.gbset import GBSet
from eutils.xmlfacades.gene import Gene
from eutils.xmlfacades.pubmed import PubMedArticle

default_cache_path = os.path.join(os.path.expanduser('~'),'.cache','eutils-cache.db')


class Client(object):

    def __init__(self,
                 cache_path=default_cache_path,
                 ):
        self._qs = QueryService(cache_path=cache_path)
        self.databases = self.einfo().databases


    def einfo(self,db=None):
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
            return EInfo( self._qs.einfo() )
        return EInfoDB( self._qs.einfo({'db':db, 'version':'2.0'}) )
        

    def esearch(self,db,term):
        """query the esearch endpoint
        """
        return ESearchResults( self._qs.esearch({'db':db,'term':term}) )


    def efetch(self,db,id):
        """query the efetch endpoint
        """
        db = db.lower()
        xml = self._qs.efetch({'db':db,'id':str(id)})
        if db in ['gene']:
            return Gene(xml)
        if db in ['nuccore']:
            # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see gbset.py)
            return GBSet(xml)
        if db in ['pubmed']:
            return PubMedArticle(xml)
        if db in ['snp']:
            return ExchangeSet(xml)
        raise EutilsError('database {db} is not currently supported by eutils'.format(db=db))
