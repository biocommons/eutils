# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree

import eutils.xmlfacades.base
from eutils.xmlfacades.gbseq import GBSeq


class GBSet(eutils.xmlfacades.base.Base):

    _root_tag = 'GBSet'

    def __str__(self):
        return "GBSet({self.acv})".format(self=self)

    @property
    def gbseqs(self):
        return list(self)

    def __iter__(self):
        return (GBSeq(n) for n in self._xml_root.iterfind('GBSeq'))


if __name__ == "__main__":
    import os
    import lxml.etree as le

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpath = 'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml'
    path = os.path.join(data_dir, relpath)
    gbset = GBSet(le.parse(path).getroot())

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
