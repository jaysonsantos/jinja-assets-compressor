# -*- coding: utf-8 -*-

from .compressors.coffee import CoffeeScriptCompressor
from .compressors.javascript import JavaScriptCompressor
from .compressors.less import LessCompressor
from .compressors.sass import SassCompressor


class Config(dict):

    _defaults = {
        'compressor_enabled': True,
        'compressor_offline_compress': False,
        'compressor_follow_symlinks': False,
        'compressor_debug': False,
        'compressor_static_prefix': '/static/dist',
        'compressor_source_dirs': None,
        'compressor_static_prefix_precompress': '/static',
        'compressor_output_dir': 'static/dist',
        'compressor_ignore_blueprint_prefix': False,
        'compressor_classes': {
            'text/css': LessCompressor,
            'text/coffeescript': CoffeeScriptCompressor,
            'text/less': LessCompressor,
            'text/javascript': JavaScriptCompressor,
            'text/sass': SassCompressor,
            'text/scss': SassCompressor,
        },
    }

    def __init__(self, **kwargs):
        self.update(self._defaults)
        self.update(**kwargs)

    def __getattr__(self, key):
        return self[key]
