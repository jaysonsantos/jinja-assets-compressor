# -*- coding: utf-8 -*-

class Config(object):

    defaults = {
        'compressor_enabled': True,
        'compressor_compress_offline': False,
        'compressor_debug': False,
        'compressor_static_prefix': '/static/dist',
        'compressor_source_dirs': None,
        'compressor_output_dir': 'static/dist',
        'compressor_ignore_blueprint_prefix': False,
    }

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
        for key, val in self.defaults.items():
            setattr(self, key, kwargs.get(key, self.defaults[key]))
