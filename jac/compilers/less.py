import subprocess
from six import with_metaclass

from jac.compat import file, u, utf8_encode

from . import CompilerMeta


class LessCompiler(with_metaclass(CompilerMeta, object)):
    supported_mimetypes = ['text/less', 'text/css']

    @classmethod
    def compile(cls, what, mimetype='text/less', cwd=None, uri_cwd=None,
                debug=None):
        args = ['lessc']

        if not debug:
            args += ['--compress']

        if cwd:
            args += ['-ru']
            args += ['--include-path={}'.format(cwd)]

        if uri_cwd:
            if not uri_cwd.endswith('/'):
                uri_cwd += '/'
            args += ['--rootpath={}'.format(uri_cwd)]

        args += ['-']

        handler = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=None)

        if isinstance(what, file):
            what = what.read()
        (stdout, stderr) = handler.communicate(input=utf8_encode(what))
        stdout = u(stdout)

        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
