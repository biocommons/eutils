# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.genecommentarygenomiccoords import GeneCommentaryGenomicCoords


class GeneCommentary(Base):
    """This class  a rudimentary interface for using "Gene-commentary" XML
    nodes in NCBI efetch replies.

    We're particularly focused on two kinds of G-c nodes: the
    "reference", which is higher in the XML tree, and the "product",
    which is a descendant of the reference.

    """

    _root_tag = 'Gene-commentary'

    def __unicode__(self):
        return "TODO"

    @property
    def type(self):
        return self._xml_elem.find('Gene-commentary_type').get("value")

    @property
    def heading(self):
        return self._xml_elem.findtext('Gene-commentary_heading')

    @property
    def label(self):
        return self._xml_elem.findtext('Gene-commentary_label')

    @property
    def accession(self):
        return self._xml_elem.findtext('Gene-commentary_accession')

    @property
    def version(self):
        return self._xml_elem.findtext('Gene-commentary_version')

    @property
    def acv(self):
        if self.accession is None or self.version is None:
            return None
        return self.accession + '.' + self.version

    @property
    def products(self):
        return [GeneCommentary(gc) for gc in self._xml_elem.xpath('Gene-commentary_products/Gene-commentary')]

    @property
    def genomic_coords(self):
        gcgcs = self._xml_elem.xpath('Gene-commentary_genomic-coords')
        if len(gcgcs) == 0:
            return None
        assert len(gcgcs) == 1
        return GeneCommentaryGenomicCoords(gcgcs[0])


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
