# -*- coding: utf-8 -*-

import subprocess
from rjsmin import jsmin

from jac.compat import file, u, utf8_encode


class CoffeeScriptCompressor(object):
    """Builtin compressor text/coffeescript mimetype.

    Uses the coffee command line program to generate JavaScript, then
    uses rjsmin for minification.
    """

    @classmethod
    def compile(cls, what, mimetype='text/coffeescript', cwd=None, uri_cwd=None, debug=None):

        args = ['coffee', '--compile', '--stdio']

        handler = subprocess.Popen(
            args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=None)

        if isinstance(what, file):
            what = what.read()

        (stdout, stderr) = handler.communicate(input=utf8_encode(what))
        stdout = u(stdout)

        if not debug:
            stdout = jsmin(stdout)

        if handler.returncode == 0:
            return stdout
        else:
            raise RuntimeError('Test this :S %s' % stderr)
