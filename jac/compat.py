# -*- coding: utf-8 -*-

import codecs
import io
import sys


is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

if is_py2:

    def _u(text):
        if isinstance(text, str):
            return text.decode('utf-8')
        return unicode(text)
    u = _u
    open = codecs.open
    basestring = basestring
    file = (file, codecs.Codec, codecs.StreamReaderWriter)

elif is_py3:

    u = str
    open = open
    basestring = (str, bytes)
    file = io.IOBase
