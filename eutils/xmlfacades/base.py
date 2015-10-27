# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import lxml.etree

from eutils.exceptions import EutilsError

logger = logging.getLogger(__name__)

class Base(object):
    """Root class for all xmlfacade classes.

    This class is instantiated only by subclasses.

    xmlfacades must be instantiated with an XML document, passed
    either as XML text or as the root of a parsed XML document.

    _root_tag must be defined by the subclass. It is used to validate
    the node type upon instantiation of the subclass.

    """

    _root_tag = None

    def __init__(self, xml):
        if isinstance(xml, lxml.etree._Element):
            self._xml_root = xml
        elif isinstance(xml, str) or isinstance(xml, bytes):
            self._xml_root = lxml.etree.XML(xml)
        else:
            raise EutilsError("Cannot create object from type " + type(xml).__name__)

        if self._root_tag is None:
            raise EutilsError("_root_tag not defined for class {}".format(type(self).__name__))
        elif self._root_tag != self._xml_root.tag:
            raise EutilsError("XML for {} object must be a {} element (got {})".format(
                type(self).__name__, self._root_tag, self._xml_root.tag))


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
