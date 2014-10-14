# -*- coding: utf-8 -*-

from rjsmin import jsmin
from six import with_metaclass

from . import CompilerMeta


class JavaScriptCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/javascript']

    @classmethod
    def compile(cls, what, mimetype='text/javascript', cwd=None,
                uri_cwd=None, debug=None):
        if debug:
            return what
        return jsmin(what)
