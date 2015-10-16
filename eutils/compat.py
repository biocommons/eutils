"""compat.py

Attempts to quarantine as much python 2 / python 3 compatibility debris as possible.

Available methods:

  * ...

Available py2k/py3k "compatified" imports:

  * pickle  (synonymizes py2's cPickle and py3's pickle)

"""

import six

if six.PY2:
    import cPickle as pickle
else:
    import pickle

