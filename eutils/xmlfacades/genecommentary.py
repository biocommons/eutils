# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.exceptions import EutilsError
import eutils.xmlfacades.base

class GeneCommentary(eutils.xmlfacades.base.Base):
    """This class  a rudimentary interface for using "Gene-commentary" XML
    nodes in NCBI efetch replies.

    We're particularly focused on two kinds of G-c nodes: the
    "reference", which is higher in the XML tree, and the "product",
    which is a descendant of the reference.

    IMO, Gene-commentary and friends stand out as examples of fatuous
    overdesign in the great trainwreck that is NCBI's XML.

    """

    _root_tag = 'Gene-commentary'

    def __str__(self):
        return 'GeneCommentary(acv={self.acv},type={self.type},heading={self.heading},label={self.label})'.format(self=self)

    @property
    def accession(self):
        return self._xml_root.findtext('Gene-commentary_accession')

    @property
    def acv(self):
        if self.accession is None or self.version is None:
            return None
        return self.accession + '.' + self.version

    @property
    def genomic_coords(self):
        n = self._xml_root.find("Gene-commentary_genomic-coords")
        if n is None:
            raise EutilsError("this object (type={self.type}) does not have genomic coordinates defined (mRNA and peptide typically do)".format(self=self))
        return GeneCommentaryGenomicCoords(n)

    @property
    def heading(self):
        return self._xml_root.findtext('Gene-commentary_heading')

    @property
    def label(self):
        return self._xml_root.findtext('Gene-commentary_label')

    @property
    def products(self):
        return [GeneCommentary(gc) for gc in self._xml_root.findall('Gene-commentary_products/Gene-commentary')]

    @property
    def type(self):
        return self._xml_root.find('Gene-commentary_type').get("value")

    @property
    def version(self):
        return self._xml_root.findtext('Gene-commentary_version')


class GeneCommentaryGenomicCoords(eutils.xmlfacades.base.Base):
    """This class  a rudimentary interface for using "Gene-commentary_genomic-coords" XML
    nodes in NCBI eutilities (efetch) responses.
    """

    _root_tag = 'Gene-commentary_genomic-coords'

    def __str__(self):
        return "{self.gi}:{self.strand}:{self._interval_str}".format(self=self)

    @property
    def strand(self):
        nastrand = self._xml_root.find('.//Na-strand').get('value')
        return 1 if nastrand == 'plus' else -1 if nastrand == 'minus' else None

    @property
    def gi(self):
        return self._xml_root.findtext('.//Seq-id_gi')

    @property
    def intervals(self):
        return [(i.interval_from, i.interval_to)
                for i in (SeqInterval(n) for n in self._xml_root.findall('.//Seq-interval'))]

    @property
    def _interval_str(self):
        return ';'.join(str(i) for i in self.intervals)


class SeqInterval(eutils.xmlfacades.base.Base):

    _root_tag = 'Seq-interval'

    def __str__(self):
        return "[{self.interval_from},{self.interval_to}]".format(self=self)

    @property
    def interval_from(self):
        return int(self._xml_root.findtext('Seq-interval_from'))

    @property
    def interval_to(self):
        return int(self._xml_root.findtext('Seq-interval_to'))


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
