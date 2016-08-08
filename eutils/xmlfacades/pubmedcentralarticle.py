# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.utils import xml_get_text_or_none, xml_get1
import eutils.xmlfacades.base


class PubmedCentralArticle(eutils.xmlfacades.base.Base):

    _root_tag = 'article'

    def __str__(self):
        return ('{pmca.__class__.__name__}(pmc={pmca.pmc};pmid={pmca.pmid};doi={pmca.doi};{pmca.title})'.format(pmca=self))

    @property
    def title(self):
        return ''.join([x for x in xml_get1(self._xml_root, 'front/article-meta/title-group/article-title').itertext()])

    @property
    def abstract_text(self):
        return ''.join([x for x in xml_get1(self._xml_root, 'front/article-meta/abstract').itertext()])

    @property
    def body_text(self):
        body = self._xml_root.xpath('body')
        if body:
            parts = [x for x in body[0].itertext()]
            return ''.join(parts)
        else:
            return None

    @property
    def doi(self):
        return xml_get_text_or_none(self._xml_root, 'front/article-meta/article-id[@pub-id-type="doi"]')

    @property
    def pmid(self):
        return xml_get_text_or_none(self._xml_root, 'front/article-meta/article-id[@pub-id-type="pmid"]')

    @property
    def pmc(self):
        return xml_get_text_or_none(self._xml_root, 'front/article-meta/article-id[@pub-id-type="pmc"]')


if __name__ == "__main__":
    from eutils.xmlfacades.pubmedcentralarticleset import PubmedCentralArticleSet
    import lxml.etree as le
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpaths = [
        'efetch.fcgi?db=pmc&id=3299399&rettype=xml.xml', 'efetch.fcgi?db=pmc&id=3299399&retmode=xml.xml',
        'efetch.fcgi?db=pmc&id=3299399&retmode=xml.xml'
    ]
    path = os.path.join(data_dir, relpaths[0])
    pmcas = PubmedCentralArticleSet(le.parse(path).getroot())
    pmca = next(iter(pas))

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
