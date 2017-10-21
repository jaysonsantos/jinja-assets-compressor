# -*- coding: utf-8 -*-

import errno
import subprocess

from jac.compat import file
from jac.compat import u
from jac.compat import utf8_encode
from jac.exceptions import InvalidCompressorError


class SassCompressor(object):
    """Builtin compressor for text/sass and text/scss mimetypes.

    Uses the sass command line program for compression.
    """

    binary = 'sass'
    extra_args = []

    @classmethod
    def compile(cls, what, mimetype='text/sass', cwd=None, uri_cwd=None,
                debug=None):
        args = ['-s']
        if mimetype == 'text/scss':
            args.append('--scss')

        if cwd:
            args += ['-I', cwd]

        if cls.extra_args:
            args.extend(cls.extra_args)

        args.insert(0, cls.binary)

        try:
            handler = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=None)
        except OSError as e:
            msg = '{0} encountered an error when executing {1}: {2}'.format(
                cls.__name__,
                cls.binary,
                u(e),
            )
            if e.errno == errno.ENOENT:
                msg += ' Make sure {0} is in your PATH.'.format(cls.binary)
            raise InvalidCompressorError(msg)

        if isinstance(what, file):
            what = what.read()
        (stdout, stderr) = handler.communicate(input=utf8_encode(what))
        stdout = u(stdout)

        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
