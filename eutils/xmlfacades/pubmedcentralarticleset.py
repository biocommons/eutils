# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import eutils.xmlfacades.base
from eutils.xmlfacades.pubmedcentralarticle import PubmedCentralArticle


class PubmedCentralArticleSet(eutils.xmlfacades.base.Base):

    _root_tag = 'pmc-articleset'

    def __iter__(self):
        return (PubmedCentralArticle(pmca_n) for pmca_n in self._xml_root.iterfind('article'))


if __name__ == "__main__":
    import os
    import lxml.etree as le

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpaths = [
        'efetch.fcgi?db=pmc&id=3299399&rettype=xml.xml', 'efetch.fcgi?db=pmc&id=3299399&retmode=xml.xml',
        'efetch.fcgi?db=pmc&id=3299399&retmode=xml.xml'
    ]

    pmcasets = [PubmedCentralArticleSet(le.parse(os.path.join(data_dir, relpath)).getroot()) for relpath in relpaths]

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
