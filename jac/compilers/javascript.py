from rjsmin import jsmin
from six import with_metaclass

from . import CompilerMeta


class JavaScriptCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/javascript']

    @classmethod
    def compile(cls, what, mimetype='text/javascript', cwd=None,
                uri_cwd=None, debug=None):
        return jsmin(what)
