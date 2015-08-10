# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
"""Provides support for parsing NCBI einfo queries as described here:

http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EInfo

Unfortunately, the reply from this endpoint is has two very different
modes: if called without an argument, it returns a list of databases;
if called with a single db= argument, it returns details about the
database.  That means that the client interface is necessarily very
different.

TODO: Implement classes for each and return appropriate class based on
reply.

"""

import eutils.xmlfacades.base


class DbInfo(eutils.xmlfacades.base.Base):

    _root_tag = 'DbInfo'

    @property
    def dbname(self):
        return self._xml_root.findtext('DbName')

    @property
    def menuname(self):
        return self._xml_root.findtext('MenuName')

    @property
    def description(self):
        return self._xml_root.findtext('Description')

    @property
    def dbbuild(self):
        return self._xml_root.findtext('DbBuild')

    @property
    def count(self):
        return self._xml_root.findtext('Count')

    @property
    def lastupdate(self):
        return self._xml_root.findtext('LastUpdate')

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
