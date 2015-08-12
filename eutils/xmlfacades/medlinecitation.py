# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.utils import xml_get_text, xml_get_text_or_none
import eutils.xmlfacades.base


class MedlineCitation(eutils.xmlfacades.base.Base):

    _root_tag = 'MedlineCitation'

    @property
    def abstract(self):
        return self._xml_root.findtext('Article/Abstract/AbstractText')

    @property
    def authors(self):
        # N.B. Citations may have 0 authors. e.g., pmid:7550356
        # Citations may also have a 'CollectiveName' author instead of one with a forename, lastname, and initials
        def _format_author(au):
            if au.find('CollectiveName') is not None:
                return au.find('CollectiveName').text
            elif au.find('LastName') is not None and au.find('Initials') is not None:
                return au.find('LastName').text + ' ' + au.find('Initials').text
            else:
                return au.find('LastName').text

        return [_format_author(au) for au in self._xml_root.xpath('Article/AuthorList/Author')]

    @property
    def issue(self):
        return self._xml_root.findtext('Article/Journal/JournalIssue/Issue')

    @property
    def jrnl(self):
        return self._xml_root.findtext('Article/Journal/ISOAbbreviation') or self._xml_root.findtext(
            'Article/Journal/Title')

    @property
    def mesh_headings(self):
        return self._xml_root.xpath('MeshHeadingList/MeshHeading/DescriptorName/text()')

    @property
    def pages(self):
        return self._xml_root.findtext('Article/Pagination/MedlinePgn')

    @property
    def pmid(self):
        return self._xml_root.findtext('PMID')

    @property
    def title(self):
        return self._xml_root.findtext('Article/ArticleTitle')

    @property
    def volume(self):
        return self._xml_root.findtext('Article/Journal/JournalIssue/Volume')

    @property
    def year(self):
        return self._xml_root.findtext('Article/Journal/JournalIssue/PubDate/Year') \
          or self._xml_root.findtext('Article/Journal/JournalIssue/PubDate/Year') \
          or self._xml_root.findtext('Article/Journal/JournalIssue/PubDate/MedlineDate')


if __name__ == "__main__":
    import lxml.etree as le
    import os

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    path = os.path.join(data_dir, 'medlinecitation-id=20412080.xml.gz')

    mc = MedlineCitation(le.parse(path).getroot())

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
