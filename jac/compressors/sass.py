# -*- coding: utf-8 -*-

import subprocess

from jac.compat import file, u, utf8_encode


class SassCompressor(object):
    """Builtin compressor for text/sass and text/scss mimetypes.

    Uses the sass command line program for compression.
    """

    @classmethod
    def compile(cls, what, mimetype='text/sass', cwd=None,
                uri_cwd=None, debug=None):
        args = ['sass', '-s']
        if mimetype == 'text/scss':
            args.append('--scss')

        if cwd:
            args += ['-I', cwd]

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
