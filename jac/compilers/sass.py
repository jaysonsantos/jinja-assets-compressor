import subprocess

from . import CompilerMeta


class SassCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['text/sass', 'text/scss']

    @classmethod
    def compile(cls, what, mimetype='text/sass', cwd=None):
        args = ['sass', '-s']
        if mimetype == 'text/scss':
            args.append('--scss')

        handler = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=None)

        handler.stdin.write(what)
        handler.stdin.close()
        if handler.wait() == 0:
            return handler.stdout.read()
        else:
            raise RuntimeError('Test this :S %s' % handler.stderr.read())
