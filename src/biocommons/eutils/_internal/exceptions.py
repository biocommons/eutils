# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals


class EutilsError(Exception):
    """Base class for all Eutils exceptions, and also used to raise
    general exception.

    """
    pass


class EutilsNCBIError(EutilsError):
    """Raised when NCBI returns data that appears to be incorrect or
    invalid.

    """
    pass


class EutilsNotFoundError(EutilsError):
    """Raised when the requested data is not available. (Used only by the
    :mod:`eutils.sketchy.clientx` interface currently.)

    """
    pass


class EutilsRequestError(EutilsError):
    """Raised when NCBI responds with an error, such as when a non-existent
    database is specified.

    """
    pass


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
