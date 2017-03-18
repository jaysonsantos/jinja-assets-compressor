# -*- coding: utf-8 -*-

from rjsmin import jsmin


class JavaScriptCompressor(object):
    """Builtin compressor for text/javascript mimetype.

    Uses the rjsmin for minification.
    """

    @classmethod
    def compile(cls, what, mimetype='text/javascript', cwd=None, uri_cwd=None,
                debug=None):
        if debug:
            return what
        return jsmin(what)
