# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from eutils.xmlfacades.base import Base


class SeqInterval(Base):

    _root_tag = 'Seq-interval'

    def __unicode__(self):
        return 'TODO'

    @property
    def interval_from(self):
        return int(self._xml_elem.findtext('Seq-interval_from'))

    @property
    def interval_to(self):
        return int(self._xml_elem.findtext('Seq-interval_to'))

    @property
    def strand(self):
        nastrand = int(self._xml_elem.find('Seq-interval_strand/Na-strand').get('value'))
        return 1 if nastrand == 'plus' else -1 if nastrand == 'minus' else None

    @property
    def gi(self):
        return int(self._xml_elem.findtext('Seq-interval_id/Seq-id/Seq-id_gi'))


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
