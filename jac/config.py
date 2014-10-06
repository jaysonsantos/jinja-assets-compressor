# -*- coding: utf-8 -*-

class Config(object):

    defaults = {
        'compressor_enabled': True,
        'compressor_offline_compress': False,
        'compressor_follow_symlinks': False,
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
            self.set(key, kwargs.get(key, self.defaults[key]))

    def set(self, key, val):
        setattr(self, key, val)
