# -*- coding: utf-8 -*-

import os

from jac.compat import u


def static_finder(app):
    def find(path=None):
        if path is None:
            folders = set()
            for blueprint in app.blueprints.values():
                if blueprint.static_folder is not None:
                    folders.append(blueprint.static_folder)
            folders.update(list(app.static_folder))
            return folders
        else:
            for rule in app.url_map.iter_rules():
                if '.' in rule.endpoint and not app.jinja_env.compressor_ignore_blueprint_prefix:
                    with_blueprint = True
                    (blueprint, view) = rule.endpoint.split('.', 1)
                    blueprint = app.blueprints[blueprint]

                    data = rule.match(u('{subdomain}|{path}').format(
                        subdomain=blueprint.subdomain or '',
                        path=path,
                    ))
                else:
                    with_blueprint = False
                    data = rule.match(u('|{0}').format(path))

                if data:
                    static_folder = blueprint.static_folder if with_blueprint and blueprint.static_folder is not None else app.static_folder
                    return os.path.join(static_folder, data['filename'])

            raise IOError(2, u('File not found {0}.').format(path))

    return find


class JAC(object):
    """Simple helper class for Jinja Assets Compressor. Has to be created in
    advance like a :class:`~flask.Flask` object.

    There are two usage modes which work very similar.  One is binding
    the instance to a very specific Flask application::

        app = Flask(__name__)
        jac = JAC(app)

    The second possibility is to create the object once and configure the
    application later to support it::

        jac = JAC()

        def create_app():
            app = Flask(__name__)
            jac.init_app(app)
            return app

    :param app: the application to register.
    """

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.add_extension('jac.CompressorExtension')
        app.jinja_env.compressor_enabled = app.config.get('COMPRESSOR_ENABLED', True)
        app.jinja_env.compressor_offline_compress = app.config.get('COMPRESSOR_OFFLINE_COMPRESS', False)
        app.jinja_env.compressor_follow_symlinks = app.config.get('COMPRESSOR_FOLLOW_SYMLINKS', False)
        app.jinja_env.compressor_debug = app.config.get('COMPRESSOR_DEBUG', False)
        app.jinja_env.compressor_output_dir = app.config.get('COMPRESSOR_OUTPUT_DIR') or app.static_folder
        app.jinja_env.compressor_static_prefix = app.config.get('COMPRESSOR_STATIC_PREFIX') or app.static_url_path
        app.jinja_env.compressor_ignore_blueprint_prefix = app.config.get('COMPRESSOR_IGNORE_BLUEPRINT_PREFIX', False)
        app.jinja_env.compressor_source_dirs = static_finder(app)
