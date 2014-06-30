# -*- coding: utf-8 -*-

import codecs
import sys


is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

if is_py2:

    def _u(text):
        if type(text) == str:
            return text.decode('utf-8')
        return unicode(text)
    u = _u
    open = codecs.open

elif is_py3:

    u = str
    open = open
