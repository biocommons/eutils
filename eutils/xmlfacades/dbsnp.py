# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import re

import lxml.etree

from eutils.exceptions import *
import eutils.xmlfacades.base

genome_ac_re = re.compile('^(?:NC)_')
transcript_ac_re = re.compile('^(?:ENST|NG|NM)_')
protein_ac_re = re.compile('^(?:ENSP|NP)_')


class ExchangeSet(eutils.xmlfacades.base.Base):

    _root_tag = '{http://www.ncbi.nlm.nih.gov/SNP/docsum}ExchangeSet'

    def __iter__(self):
        return (Rs(n) for n in self._xml_root.iterfind('docsum:Rs', namespaces={'docsum': self._xml_root.nsmap[None]}))

    def __len__(self):
        return len(self._xml_root.findall('docsum:Rs', namespaces={'docsum': self._xml_root.nsmap[None]}))


class Rs(object):

    _root_tag = 'Rs'

    def __init__(self, rs_node):
        assert rs_node.tag == '{http://www.ncbi.nlm.nih.gov/SNP/docsum}Rs'
        self._n = rs_node

    #def __str__(self):
    #    return "Rs({self.id})".format(self=self)

    @property
    def rs_id(self):
        return 'rs' + self._n.get('rsId')

    @property
    def withdrawn(self):
        return 'notwithdrawn' not in self._n.get('snpType')

    @property
    def orient(self):
        return self._n.get('orient')

    @property
    def strand(self):
        return self._n.get('strand')

    @property
    def hgvs_tags(self):
        return self._n.xpath('docsum:hgvs/text()', namespaces={'docsum': self._n.nsmap[None]})

    @property
    def hgvs_genome_tags(self):
        return [t for t in self.hgvs_tags if genome_ac_re.match(t)]

    @property
    def hgvs_transcript_tags(self):
        return [t for t in self.hgvs_tags if transcript_ac_re.match(t)]

    @property
    def hgvs_protein_tags(self):
        return [t for t in self.hgvs_tags if protein_ac_re.match(t)]

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
