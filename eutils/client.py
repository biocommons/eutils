# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

import lxml.etree as le

from eutils.exceptions import *
from eutils.queryservice import QueryService
from eutils.xmlfacades.dbsnp import ExchangeSet
from eutils.xmlfacades.einforesult import EInfoResult
from eutils.xmlfacades.entrezgeneset import EntrezgeneSet
from eutils.xmlfacades.esearchresult import ESearchResult
from eutils.xmlfacades.gbset import GBSet
from eutils.xmlfacades.pubmedarticleset import PubmedArticleSet
from eutils.xmlfacades.pubmedcentralarticleset import PubmedCentralArticleSet

default_cache_path = os.path.join(os.path.expanduser('~'), '.cache', 'eutils-cache.db')

logger = logging.getLogger(__name__)

class Client(object):
    """class-based access to NCBI E-Utilities, returning Python classes
    with rich data accessors

    """

    def __init__(self, cache_path=default_cache_path):
        """
        :param str cache_path: full path to sqlite database file (created if necessary)
        :raises EutilsError: if cache file couldn't be created
        """
        cache_dir = os.path.dirname(cache_path)
        if not os.path.exists(cache_dir):
            try:
                os.mkdir(cache_dir)
                logger.info("Made cache directory " + cache_dir)
            except OSError:
                raise EutilsError("Failed to make cache directory " + cache_dir)
        self._qs = QueryService(cache_path=cache_path)

    @property
    def databases(self):
        """
        list of databases available from eutils (per einfo query)
        """
        try:
            return self._databases
        except AttributeError:
            self._databases = self.einfo().databases
            return self._databases

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
        esr = ESearchResult(self._qs.esearch({'db': db, 'term': term}))
        if esr.count > esr.retmax:
            logger.warn("NCBI found {esr.count} results, but we truncated the reply at {esr.retmax}"
                        " results; see https://bitbucket.org/biocommons/eutils/issues/124/".format(esr=esr))
        return esr

    def efetch(self, db, id):
        """query the efetch endpoint
        """
        db = db.lower()
        xml = self._qs.efetch({'db': db, 'id': str(id)})
        doc = le.XML(xml)
        if db in ['gene']:
            return EntrezgeneSet(doc)
        if db in ['nuccore']:
            # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see gbset.py)
            return GBSet(doc)
        if db in ['pubmed']:
            return PubmedArticleSet(doc)
        if db in ['snp']:
            return ExchangeSet(xml)
        if db in ['pmc']:
            return PubmedCentralArticleSet(doc)
        raise EutilsError('database {db} is not currently supported by eutils'.format(db=db))


# <LICENSE>
# Copyright 2015 eutils Committers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
# </LICENSE>
