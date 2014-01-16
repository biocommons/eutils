# -*- encoding: utf-8 -*-
# License appears at end of file

"""provides XML access to NCBI E-utilities

http://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

# TODO: per-request cache and throttle settings?
# Don't cache search results
# Fetch & compare

import hashlib
import cPickle
import logging
import os
import requests
import time
import urllib2

from rcore.sqlitecache import SQLiteCache

from eutils.exceptions import *

default_tool = __package__
default_email = 'reecehart+eutils@gmail.com'
default_request_interval = 0.333
default_cache_path = os.path.join('/tmp',default_tool+'-'+str(os.getuid())+'.db')

logging.basicConfig(level=logging.DEBUG)

class EutilsClient(object):
    url_base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
    def __init__(self,
                 cache_path=default_cache_path,
                 default_args={},
                 email=default_email,
                 request_interval=default_request_interval,
                 tool=default_tool,
                 ):
        self.default_args = default_args
        self.email = email
        self.request_interval = request_interval
        self.tool = tool

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._last_request_clock = 0
        self._cache = SQLiteCache(cache_path) if cache_path else None
        self._ident_args = { 'tool': tool, 'email': email }
        self._request_count = 0


    def fetch(self,path,args={},skip_cache=False,skip_sleep=False):
        # cache key: the key associated with this endpoint and args The
        # key intentionally excludes the identifying args (tool and email)
        # and is independent of the request method (GET/POST) args are
        # sorted for canonicalization

        url = self.url_base + path
        defining_args = dict( self.default_args.items() + args.items() )
        full_args = (self._ident_args.items() + defining_args.items())
        cache_key = hashlib.md5( cPickle.dumps((url,sorted(defining_args.items()))) ).hexdigest()

        if self._cache:
            sqas = ';'.join([k+'='+v for k,v in sorted(args.items())])
            try:
                v = self._cache[cache_key]
                logging.debug('cache hit for key {cache_key} ({url}, {sqas}) '.format(
                    cache_key=cache_key, url=url, sqas=sqas))
                return v
            except KeyError:
                logging.debug('cache miss for key {cache_key} ({url}, {sqas}) '.format(
                    cache_key=cache_key, url=url, sqas=sqas))
                pass

        sleep_time = 0 if skip_sleep else min( self.request_interval, time.clock()-self._last_request_clock )
        self._logger.debug('sleeping {sleep_time:.3f}'.format(sleep_time=sleep_time))
        time.sleep(sleep_time)
        r = requests.post(url,full_args) 
        self._last_request_clock = time.clock()
        self._logger.debug('fetched {url}'.format(url=url))

        if not r.ok:
            # TODO: inspect an error response to construct a useful message
            raise EutilsRequestError(r)

        if self._cache:
            self._cache[cache_key] = r.content
            logging.debug('cached results for key {cache_key} ({url}, {sqas}) '.format(
                cache_key=cache_key, url=url, sqas=sqas))

        return r.content



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
