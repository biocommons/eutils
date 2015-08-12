# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.entrezgene import Entrezgene


class EntrezgeneSet(Base):
    """Represents a set of genes as provided with an XML reply from an
    Entrez Gene query.

    This object supports iteration, like this:

    >> doc = lxml.etree.parse("entrezgeneset.xml.gz").getroot()
    >> egs = EntrezgeneSet(doc)
    >> len(egs.entrezgenes)
    4

    """

    _root_tag = 'Entrezgene-Set'

    @property
    def entrezgenes(self):
        try:
            return self._entrezgenes
        except AttributeError:
            self._entrezgenes = [Entrezgene(n) for n in self._entrezgene_nodes()]
            return self._entrezgenes

    def _entrezgene_nodes(self):
        return self._xml_root.iterfind('Entrezgene')

    def __iter__(self):
        return (eg for eg in self.entrezgenes)

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
