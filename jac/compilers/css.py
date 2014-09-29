from six import with_metaclass

from csscompressor import compress

from jac.compat import file, utf8_encode

from . import CompilerMeta


class CssCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/css']

    @classmethod
    def compile(cls, what, mimetype='text/css', cwd=None, uri_cwd=None,
                debug=None):
        import ipdb;ipdb.set_trace()

        if isinstance(what, file):
            what = what.read()

        if debug:
            return utf8_encode(what)

        return utf8_encode(compress(what))

