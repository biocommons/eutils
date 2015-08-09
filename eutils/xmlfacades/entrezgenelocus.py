# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree as le

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.genecommentary import GeneCommentary


class EntrezgeneLocus(Base):

    _root_tag = 'Entrezgene_locus'

    def __unicode__(self):
        return "TODO: implement __unicode__ for " + __name__

    @property
    def references(self):
        return [GeneCommentary(gc) for gc in self._xml_elem.findall('Gene-commentary')]


if __name__ == "__main__":
    import os
    import lxml.etree
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    path = os.path.join(data_dir, 'entrezgeneset.xml.gz')
    doc = lxml.etree.parse(path)
    n = doc.findall('.//Entrezgene')[0]
    o = Entrezgene(n)

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
