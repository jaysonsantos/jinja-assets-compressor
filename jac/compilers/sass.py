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

        if cwd:
            args += ['-I', cwd]

        handler = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=None)

        (stdout, stderr) = handler.communicate(input=what)
        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
