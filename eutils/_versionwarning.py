"""emits a warning when imported under Python < 3.6

This module may be used by other biocommons packages

"""

import sys
import warnings

if sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python < 3.6 is now deprecated and"
        " will be dropped on 2019-03-31. See"
        " https://github.com/biocommons/org/wiki/Migrating-to-Python-3.6")
