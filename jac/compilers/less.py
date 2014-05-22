import subprocess

from . import CompilerMeta


class LessCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['text/less', 'text/css']

    @classmethod
    def compile(cls, what, mimetype='text/less', cwd=None):
        args = ['lessc', '--compress', '-']

        handler = subprocess.Popen(args, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=None)

        (stdout, stderr) = handler.communicate(input=what)
        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
