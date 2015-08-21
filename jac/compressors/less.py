# -*- coding: utf-8 -*-

import subprocess

from jac.compat import file, u, utf8_encode

class LessCompressor(object):
    """Builtin compressor for text/less and text/css mimetypes.

    Uses the lessc command line program for compression.
    """

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
