def patch_app(app):
    app.jinja_env.add_extension('jac.CompilerExtension')
    app.jina_env.compressor_output_dir = app.config['COMPRESSOR_OUTPUT_DIR']
    app.jinja_env.compressor_static_prefix = app.config['COMPRESSOR_STATIC_PREFIX']
