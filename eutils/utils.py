# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


def xml_get1(node, xpath):
    return node.xpath(xpath)[0]


def xml_get1_or_none(node, xpath):
    try:
        return xml_get1(node, xpath)
    except IndexError:
        return None


def xml_get_text(node, xpath):
    return xml_get1(node, xpath).text


def xml_get_text_or_none(node, xpath):
    try:
        return xml_get_text(node, xpath)
    except IndexError:    # xpath search found 0 matches
        return None


def xml_xpath_text(node, xpath):
    return [n.text for n in node.xpath(xpath)]


def xml_xpath_text_first(node, xpath):
    try:
        return xml_xpath_list_text(node, xpath)[0]
    except IndexError:
        return None


def arglist_to_dict(**args):
    return dict(**args)


a2d = arglist_to_dict

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
