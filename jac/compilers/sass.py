import subprocess

from . import CompilerMeta


class SassCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['text/sass', 'text/scss']

    @classmethod
    def compile(cls, what):
        handler = subprocess.Popen(['sass', '-s'], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        handler.stdin.write(what)
        handler.stdin.close()
        if handler.wait() == 0:
            return handler.stdout.read()
        else:
            raise RuntimeError('Test this :S %s' % handler.stderr.read())
