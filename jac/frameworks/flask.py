def static_finder(app):
    def find(path):
        import os

        for rule in app.url_map.iter_rules():
            data = rule.match('|%s' % path)
            if data:
                (blueprint, view) = rule.endpoint.split('.')
                blueprint = app.blueprints[blueprint]

                filename = os.path.join(blueprint.static_folder, data['filename'])

                return filename

        raise IOError(2, 'File not found %s.' % path)

    return find


def configure_app(app):
    app.jinja_env.add_extension('jac.CompilerExtension')
    app.jinja_env.compressor_output_dir = app.static_folder
    app.jinja_env.compressor_static_prefix = app.static_url_path
    app.jinja_env.compressor_source_dirs = static_finder(app)
