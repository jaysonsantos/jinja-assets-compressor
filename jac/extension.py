# -*- coding: utf-8 -*-

import os

from jinja2 import nodes
from jinja2.ext import Extension

from jac.base import Compressor
from jac.compat import u


class CompressorExtension(Extension):
    tags = set(['compress'])

    def __init__(self, *args, **kwargs):
        super(CompressorExtension, self).__init__(*args, **kwargs)
        self.compressor = Compressor(environment=self.environment)

    def parse(self, parser):

        # update configs
        configs = self.compressor.get_configs_from_environment(self.environment)
        self.compressor.config.update(**configs)

        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('Template tags not supported inside compress blocks.')

        if hasattr(self.environment, 'compressor_offline_compress') and self.environment.compressor_offline_compress:
            return nodes.CallBlock(self.call_method('_display_block', args), [], [], body).set_lineno(lineno)
        else:
            return nodes.CallBlock(self.call_method('_compress_block', args), [], [], body).set_lineno(lineno)

    def _compress_block(self, compression_type, caller):
        html = caller()
        return self.compressor.compress(html, compression_type)

    def _display_block(self, compression_type, caller):
        html = caller()
        html_hash = self.compressor.make_hash(html)
        filename = os.path.join(u('{hash}.{extension}').format(
            hash=html_hash,
            extension=compression_type,
        ))
        static_prefix = u(self.compressor.config.compressor_static_prefix)
        return self.compressor.render_element(os.path.join(static_prefix, filename), compression_type)

    def set(self, key, val):
        self.compressor.config.set(key, val)
