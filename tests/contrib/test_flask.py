# -*- coding: utf-8 -*-
import os
from unittest import mock

import pytest
from flask import Flask

from jac.contrib.flask import JAC
from jac.contrib.flask import static_finder
from tests.helpers import TempDir


@pytest.fixture
def mocked_flask_app():
    return mock.Mock()


def test_flask_extension_init_self_app(mocked_flask_app):
    ext = JAC(mocked_flask_app)
    assert ext.app is mocked_flask_app


def test_flask_extension_lazy_init(mocked_flask_app):
    """Make sure we save then app when initializing Flask with app factory."""
    ext = JAC()
    assert ext.app is None
    ext.init_app(mocked_flask_app)
    assert ext.app == mocked_flask_app


def test_flask_extension_jinja_env_add_extension(mocked_flask_app):
    ext = JAC()
    ext.init_app(mocked_flask_app)
    mocked_flask_app.jinja_env.add_extension.assert_called_once_with('jac.CompressorExtension')


def test_flask_extension_jinja_env_compressor_output_dir(mocked_flask_app):
    mocked_flask_app.static_folder = '/static/folder'
    mocked_flask_app.static_url_path = '/static'
    mocked_flask_app.config = dict()

    ext = JAC()
    ext.init_app(mocked_flask_app)
    assert mocked_flask_app.jinja_env.compressor_output_dir == '/static/folder/sdist'
    assert mocked_flask_app.jinja_env.compressor_static_prefix == '/static/sdist'


def test_flask_extension_jinja_env_static_prefix(mocked_flask_app):
    mocked_flask_app.static_folder = '/static/folder'
    mocked_flask_app.static_url_path = '/static-url'
    mocked_flask_app.config = dict()

    ext = JAC()
    ext.init_app(mocked_flask_app)
    assert mocked_flask_app.jinja_env.compressor_output_dir == '/static/folder/sdist'
    assert mocked_flask_app.jinja_env.compressor_static_prefix == '/static-url/sdist'


def test_flask_extension_jinja_env_source_dirs(mocked_flask_app):
    ext = JAC()
    ext.init_app(mocked_flask_app)
    mocked_flask_app.jinja_env.compressor_source_dirs == static_finder(mocked_flask_app)


def test_flask_extension_find_static():
    app = Flask(__name__)

    # Avoid breaking static_finder when an url is registered with an endpoint which does not match with the blueprint
    app.add_url_rule('/some/url', 'wrong.blueprint_url')

    JAC(app)
    find = static_finder(app)

    with TempDir.with_context() as temp_dir:
        static_folder = temp_dir.name
        app.static_folder = static_folder
        static_file = os.path.join(static_folder, 'some.css')
        with open(static_file, 'w') as f:
            f.write('html {}')
        # This should be findable even if some urls' endpoints use broken names
        assert find('/static/some.css') == static_file
