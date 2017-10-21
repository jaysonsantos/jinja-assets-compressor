# -*- coding: utf-8 -*-

import errno
import subprocess

from jac.compat import file
from jac.compat import u
from jac.compat import utf8_encode
from jac.exceptions import InvalidCompressorError


class LessCompressor(object):
    """Builtin compressor for text/less and text/css mimetypes.

    Uses the lessc command line program for compression.
    """

    binary = 'lessc'
    extra_args = []

    @classmethod
    def compile(cls, what, mimetype='text/less', cwd=None, uri_cwd=None,
                debug=None):
        args = []

        if not debug:
            args += ['--compress']

        if cwd:
            args += ['-ru']
            args += ['--include-path={}'.format(cwd)]

        if uri_cwd:
            if not uri_cwd.endswith('/'):
                uri_cwd += '/'
            args += ['--rootpath={}'.format(uri_cwd)]

        if cls.extra_args:
            args.extend(cls.extra_args)

        args += ['-']

        args.insert(0, cls.binary)

        try:
            handler = subprocess.Popen(args,
                                       stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
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
