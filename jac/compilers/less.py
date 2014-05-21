import subprocess

from . import CompilerMeta


class LessCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['text/less', 'text/css']

    @classmethod
    def compile(cls, what, mimetype='text/less', cwd=None):
        return what
