# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree

from eutils.exceptions import *
from eutils.xmlfacades.base import Base

# TODO: implement results iterator
# once these objects contain a reference to the client,
# we'll be able to iterate using the webenv history
# See here:
# http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Demonstration_Programs
# for($retstart = 0; $retstart < $Count; $retstart += $retmax) {
#   my $efetch = "$utils/efetch.fcgi?" .
#                "rettype=$report&retmode=text&retstart=$retstart&retmax=$retmax&" .
#                "db=$db&query_key=$QueryKey&WebEnv=$WebEnv";


class ESearchResult(Base):

    _root_tag = 'eSearchResult'

    @property
    def count(self):
        return int(self._xml_elem.find('Count').text)

    @property
    def retmax(self):
        return int(self._xml_elem.find('RetMax').text)

    @property
    def retstart(self):
        return int(self._xml_elem.find('RetStart').text)

    @property
    def ids(self):
        return [int(id) for id in self._xml_elem.xpath('/eSearchResult/IdList/Id/text()')]

    @property
    def webenv(self):
        try:
            return self._xml_elem.find('WebEnv').text
        except AttributeError:
            return None

    ############################################################################
    ## Internals
    @classmethod
    def _validate_xml(xml):
        """See Base.__init__ for explanation"""
        if '</eSearchResult>' not in xml:
            raise EutilsNCBIError("received malformed ESearchResult reply")


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
