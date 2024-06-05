# -*- coding: utf-8 -*-
from importlib.metadata import PackageNotFoundError, version

from ._internal.client import Client
from ._internal.exceptions import (
    EutilsError,
    EutilsNCBIError,
    EutilsNotFoundError,
    EutilsRequestError,
)
from ._internal.queryservice import QueryService

__all__ = [
    "Client",
    "EutilsError",
    "EutilsNCBIError",
    "EutilsNotFoundError",
    "EutilsRequestError",
    "QueryService",
]

try:
    __version__ = version(__package__)
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    __version__ = None

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
