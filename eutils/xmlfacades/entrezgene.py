# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree as le

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.genecommentary import GeneCommentary


class Entrezgene(Base):

    _root_tag = 'Entrezgene'

    def __str__(self):
        return "Entrezgene(id={self.gene_id};hgnc={self.hgnc};description={self.description};type={self.type})".format(self=self)

    @property
    def common_tax(self):
        return self._xml_root.findtext('Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_common')

    @property
    def description(self):
        return self._xml_root.findtext('Entrezgene_gene/Gene-ref/Gene-ref_desc')

    @property
    def gene_id(self):
        return int(self._xml_root.findtext('Entrezgene_track-info/Gene-track/Gene-track_geneid'))

    @property
    def gene_commentaries(self):
        try:
            return self._gene_commentaries
        except AttributeError:
            self._gene_commentaries = [GeneCommentary(n) for n in  self._xml_root.iterfind('Entrezgene_locus/Gene-commentary')]
            return self._gene_commentaries

    @property
    def genus_species(self):
        return self._xml_root.xpath('Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_taxname/text()')[0]

    @property
    def hgnc(self):
        return self._xml_root.findtext('Entrezgene_gene/Gene-ref/Gene-ref_locus')

    @property
    def locus(self):
        n = self._xml_root.find('Entrezgene_locus')
        return None if n is None else EntrezgeneLocus(n)

    @property
    def maploc(self):
        return self._xml_root.findtext('Entrezgene_gene/Gene-ref/Gene-ref_maploc')

    # references is a synonym for gene_commentaries
    references = gene_commentaries

    @property
    def tax_id(self):
        return int(self._xml_root.xpath(
            'Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_db/'
            'Dbtag[Dbtag_db/text()="taxon"]/Dbtag_tag/Object-id/Object-id_id/text()')[0])

    @property
    def summary(self):
        return self._xml_root.findtext('Entrezgene_summary')

    @property
    def synonyms(self):
        return self._xml_root.xpath('Entrezgene_gene/Gene-ref/Gene-ref_syn/Gene-ref_syn_E/text()')

    @property
    def type(self):
        return self._xml_root.find('Entrezgene_type').get("value")


if __name__ == "__main__":
    import os
    import lxml.etree
    from eutils.xmlfacades.entrezgeneset import EntrezgeneSet
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    data_file = os.path.join(data_dir, 'entrezgeneset.xml.gz')
    egs = EntrezgeneSet(le.parse(data_file).getroot())


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
