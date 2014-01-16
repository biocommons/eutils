# -*- encoding: utf-8 -*-
# License appears at end of file

"""provides XML access to NCBI E-utilities

http://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

# TODO: per-request cache and throttle settings?
# Don't cache search results
# Fetch & compare

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

logging.basicConfig()

class Client(object):
    url_base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils'
    def __init__(self,tool=default_tool,email=default_email,
                 request_interval=default_request_interval,
                 cache_path=default_cache_path):
        self.tool = tool
        self.email = email
        self.request_interval = request_interval

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._last_request_clock = 0
        self._request_count = 0
        self._cache = SQLiteCache(cache_path) if cache_path else None


    def einfo_url(self,qa={}):
        return self._make_url('/einfo.fcgi',qa)

    def einfo(self,qa={}):
        return self._get(self.einfo_url(qa))


    def esearch(self,db,term):
        # URL encode, space->'+',use post
        pass

    def efetch(self):
        pass



    def _make_url(self,path,qa):
        # TODO: url encode
        return self.url_base + path + '?' + '&'.join([
            k + '=' + v
            for k,v in sorted(qa.iteritems())])

    def _get(self,url,skip_cache=False,skip_sleep=False):
        if self._cache:
            try:
                v = self._cache[url]
                logging.debug('cache hit for '+url)
                return v
            except KeyError:
                logging.debug('cache miss for '+url)
                pass

        sleep_time = 0 if skip_sleep else min( self.request_interval, time.clock()-self._last_request_clock )
        self._logger.debug('sleeping {sleep_time:.3f}'.format(sleep_time=sleep_time))
        time.sleep(sleep_time)
        r = requests.get(url) 
        self._logger.debug('fetched {url}'.format(url=url))
        self._last_request_clock = time.clock()

        if not r.ok:
            # TODO: inspect an error response to construct a useful message
            raise EutilsRequestError(r)

        if self._cache:
            self._cache[url] = r.content

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
