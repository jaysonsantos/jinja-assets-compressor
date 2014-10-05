# -*- coding: utf-8 -*-

from six import with_metaclass

from csscompressor import compress

from jac.compat import file, utf8_encode

from . import CompilerMeta


class CssCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/css']

    @classmethod
    def compile(cls, what, mimetype='text/css', cwd=None, uri_cwd=None,
                debug=None):

        if isinstance(what, file):
            what = what.read()

        if debug:
            return what

        return compress(what)

