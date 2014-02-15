# -*- encoding: utf-8 -*-
# License appears at end of file

"""provides XML access to NCBI E-utilities

http://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

# TODO: Fetch & compare
# TODO: TTL support in cache, request-specific TTLs?
# TODO: optional db -> options map (esp. for rettype & retmode)
# TODO: deal with caching status 200 replies that are bogus (e.g., truncated xml) -- callbacks?


import datetime
import hashlib
import cPickle
import logging
import os
import time
import urllib2

import lxml
import pytz
import requests

from eutils.sqlitecache import SQLiteCache
from eutils.exceptions import *

logging.basicConfig(level=logging.DEBUG)

default_default_args = {'retmode': 'xml', 'usehistory': 'y', 'retmax': 250}
default_tool = __package__ or 'interactive'
default_email = 'reecehart+eutils@gmail.com'
default_request_interval = 0.333
default_cache_path = os.path.join(os.path.expanduser('~'),'.cache','eutils-cache.db')

eastern_tz = pytz.timezone('US/Eastern')
def time_dep_request_interval(utc_dt=None):
    # From http://www.ncbi.nlm.nih.gov/books/NBK25497/:
    # "In order not to overload the E-utility servers, NCBI recommends that
    # users post no more than three URL requests per second and limit
    # large jobs to either weekends or between 9:00 PM and 5:00 AM Eastern
    # time during weekdays."
    # Translation: Weekdays 0500-2100 => 0.333s between requests; no throttle otherwise
    if utc_dt is None:
        utc_dt = datetime.datetime.utcnow()
    eastern_dt = eastern_tz.fromutc( utc_dt )
    return default_request_interval if (0<=eastern_dt.weekday()<=4 and 5<=eastern_dt.hour<21) else 0

class QueryService(object):
    url_base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
    def __init__(self,
                 cache_path=default_cache_path,
                 default_args=default_default_args,
                 email=default_email,
                 request_interval=time_dep_request_interval,
                 tool=default_tool,
                 ):
        self.default_args = default_args
        self.email = email
        self.request_interval = request_interval
        self.tool = tool

        self._logger = logging.getLogger(__name__)
        self._last_request_clock = 0
        self._cache = SQLiteCache(cache_path) if cache_path else None
        self._ident_args = { 'tool': tool, 'email': email }
        self._request_count = 0


    def efetch(self,args={}):
        return self._fetch('/efetch.fcgi',args)

    def egquery(self,args={}):
        return self._fetch('/egquery.fcgi',args)

    def einfo(self,args={}):
        return self._fetch('/einfo.fcgi',args)

    def elink(self,args={}):
        return self._fetch('/elink.fcgi',args)

    def epost(self,args={}):
        return self._fetch('/epost.fcgi',args)

    def esearch(self,args={}):
        return self._fetch('/esearch.fcgi',args)

    def esummary(self,args={}):
        return self._fetch('/esummary.fcgi',args)


    ############################################################################
    ## Internals
    def _fetch(self,path,args={},skip_cache=False,skip_sleep=False):
        """return results for a NCBI query, possibly from the cache

        :param: path: relative query path (e.g., 'einfo.fcgi')
        :param: args: dictionary of query args
        :param: skip_cache: whether to bypass the cache on reading
        :param: skip_sleep: whether to bypass query throttling
        :rtype: xml string

        The args are joined with args required by NCBI (tool and email
        address) and with the default args declared when instantiating
        the client.
        """
        # cache key: the key associated with this endpoint and args The
        # key intentionally excludes the identifying args (tool and email)
        # and is independent of the request method (GET/POST) args are
        # sorted for canonicalization

        url = self.url_base + path
        defining_args = dict( self.default_args.items() + args.items() )
        full_args = (self._ident_args.items() + defining_args.items())
        cache_key = hashlib.md5( cPickle.dumps((url,sorted(defining_args.items()))) ).hexdigest()
        sqas = ';'.join([k+'='+str(v) for k,v in sorted(args.items())])

        if not skip_cache and self._cache:
            try:
                v = self._cache[cache_key]
                self._logger.debug('cache hit for key {cache_key} ({url}, {sqas}) '.format(
                    cache_key=cache_key, url=url, sqas=sqas))
                return v
            except KeyError:
                self._logger.debug('cache miss for key {cache_key} ({url}, {sqas}) '.format(
                    cache_key=cache_key, url=url, sqas=sqas))
                pass

        if not skip_sleep:
            req_int = self.request_interval() if callable(self.request_interval) else self.request_interval
            sleep_time = req_int - (time.clock()-self._last_request_clock)
            if sleep_time > 0:
                self._logger.debug('sleeping {sleep_time:.3f}'.format(sleep_time=sleep_time))
                time.sleep(sleep_time)
        r = requests.post(url,full_args) 
        self._last_request_clock = time.clock()
        self._logger.debug('post({url}, {sqas}): {r.status_code} {r.reason}, {len})'.format(
            url=url,sqas=sqas,r=r,len=len(r.text)))

        if not r.ok or any(bad_word in r.text for bad_word in ['<error>','<ERROR>']):
            # TODO: discriminate between types of errors
            xml = lxml.etree.fromstring(r.text.encode('utf-8'))
            raise EutilsRequestError( '{r.reason} ({r.status_code}): {error}'.format(
                r=r, error=xml.find('ERROR').text))

        if self._cache:
            # N.B. we cache the read even if skip_cache is true
            self._cache[cache_key] = r.content
            self._logger.info('cached results for key {cache_key} ({url}, {sqas}) '.format(
                cache_key=cache_key, url=url, sqas=sqas))

        return r.content


if __name__ == '__main__':
    ec = EutilsClient()
    r = ec._fetch('/einfo.fcgi',{'db':'protein'})


# <LICENSE>
# Copyright 2014 eutils Contributors
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
