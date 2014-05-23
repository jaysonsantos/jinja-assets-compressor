from rjsmin import jsmin

from . import CompilerMeta


class JavaScriptCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['text/javascript']

    @classmethod
    def compile(cls, what, mimetype='text/javascript', cwd=None,
                uri_cwd=None, debug=None):
        return jsmin(what)
