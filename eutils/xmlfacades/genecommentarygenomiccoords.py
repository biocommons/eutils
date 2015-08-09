# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.seqinterval import SeqInterval


class GeneCommentaryGenomicCoords(Base):
    """This class  a rudimentary interface for using "Gene-commentary_genomic-coords" XML
    nodes in NCBI eutilities (efetch) responses.
    """

    _root_tag = 'Gene-commentary_genomic-coords'

    @property
    def strand(self):
        nastrand = self._xml_elem.find('.//Na-strand').get('value')
        return 1 if nastrand == 'plus' else -1 if nastrand == 'minus' else None

    @property
    def gi(self):
        return self._xml_elem.findtext('.//Seq-id_gi')

    @property
    def intervals(self):
        return [SeqInterval(n) for n in self._xml_elem.findall('.//Seq-interval')]


if __name__ == "__main__":
    import gzip
    import os
    import lxml.etree
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    data_file = os.path.join(data_dir, 'entrezgeneset.xml.gz')
    doc = lxml.etree.parse(gzip.open(data_file))
    gcgc_e = doc.findall('.//Gene-commentary_genomic-coords')[0]
    gcgc = GeneCommentaryGenomicCoords(gcgc_e)


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
