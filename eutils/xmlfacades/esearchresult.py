# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree

from eutils.exceptions import *
from eutils.xmlfacades.base import Base


class ESearchResult(Base):

    _root_tag = 'eSearchResult'

    @property
    def count(self):
        return int(self._xml_root.find('Count').text)

    @property
    def retmax(self):
        return int(self._xml_root.find('RetMax').text)

    @property
    def retstart(self):
        return int(self._xml_root.find('RetStart').text)

    @property
    def ids(self):
        return [int(id) for id in self._xml_root.xpath('/eSearchResult/IdList/Id/text()')]

    @property
    def webenv(self):
        try:
            return self._xml_root.find('WebEnv').text
        except AttributeError:
            return None


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
