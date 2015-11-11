# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""compat.py

Attempts to quarantine as much python 2 / python 3 compatibility debris as possible.

Available py2k/py3k "compatified" imports:

  * pickle  (synonymizes py2's cPickle and py3's pickle)

"""
#Available methods (none yet):
#
#  * ... (add and explain here)
#

import six

if six.PY2:
    import cPickle as pickle
else:
    import pickle

