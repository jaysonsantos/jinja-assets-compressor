# -*- coding: utf-8 -*-

import codecs
import io
import sys

is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)

if is_py2:
    def u(text):
        if isinstance(text, str):
            return text.decode('utf-8')
        return unicode(text)  # noqa

    def utf8_encode(text):
        if isinstance(text, unicode):  # noqa
            return text.encode('utf-8')
        return text

    open = codecs.open
    basestring = basestring  # noqa
    file = (file, codecs.Codec, codecs.StreamReaderWriter)  # noqa

elif is_py3:
    def u(text):
        if isinstance(text, bytes):
            return text.decode('utf-8')
        return str(text)

    def utf8_encode(text):
        if isinstance(text, str):
            return text.encode('utf-8')
        return text
    open = open
    basestring = (str, bytes)
    file = io.IOBase
