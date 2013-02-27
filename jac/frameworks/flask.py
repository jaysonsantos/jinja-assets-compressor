import types


def patch_app(app):
    old_jinja_options = app.jinja_options
    new_options = dict(old_jinja_options)
    new_options['extensions'].append('jac.CompilerExtension')
    old_function = app.create_jinja_environment

    def create_jinja_environment(self):
        rv = old_function()

        rv.compressor_output_dir = self.config.COMPRESSOR_OUTPUT_DIR
        rv.compressor_static_prefix = self.config.COMPRESSOR_STATIC_PREFIX
        return rv

    app.create_jinja_environment = types.MethodType(create_jinja_environment, app, app.__class__)
