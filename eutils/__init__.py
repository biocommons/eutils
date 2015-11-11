# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import pkg_resources
import warnings

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound as e:
    warnings.warn("can't get __version__ because %s package isn't installed" % __package__, Warning)
    __version__ = None


if False:
    # This block is under consideration
    # Pros: simplified use: just import eutils and move on
    # Cons: having code appear to be in two places (e.g.,
    # eutils.Client and eutils.client.Client) is problematic in sphinx
    # and likely creates user confusion.
    from eutils.client import Client
    from eutils.exceptions import EutilsError, EutilsNCBIError, EutilsNotFoundError, EutilsRequestError
    from eutils.queryservice import QueryService
    __all__ = [
        'Client', 'QueryService', 'EutilsError',
        'EutilsNCBIError', 'EutilsNotFoundError', 'EutilsRequestError']


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
