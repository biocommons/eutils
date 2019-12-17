"""emits a warning when imported under Python < 3.6

This module may be used by other biocommons packages

"""

import logging
import sys

__all__ = []

version_warning = ("biocommons packages are tested and supported only on Python >= 3.6"
                   " (https://github.com/biocommons/org/wiki/Migrating-to-Python-3.6)")

if sys.version_info < (3, 6):
    logging.warning(version_warning)
    
