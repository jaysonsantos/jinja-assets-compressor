# -*- coding: utf-8 -*-

import os

from jinja2 import nodes
from jinja2.ext import Extension

from jac.base import JAC


class CompilerExtension(Extension):
    tags = set(['compress'])

    def __init__(self, *args, **kwargs):
        super(CompilerExtension, self).__init__(*args, **kwargs)
        options = self._get_settings()
        self.jac = JAC(**options)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('One tag supported for now.')

        return nodes.CallBlock(self.call_method('_compress_block', args), [], [], body).set_lineno(lineno)

    def _compress_block(self, compression_type, caller):
        html = caller()
        return self.jac.compress(html, compression_type)

    def _get_settings(self):
        settings = {}
        for key in dir(self.environment):
            if key.startswith('compressor_'):
                settings[key] = getattr(self.environment, key)
        return settings
