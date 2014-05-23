# -*- coding: utf-8 -*-
from jac.contrib.flask import JAC, static_finder
import mock
import pytest


@pytest.fixture
def mocked_flask_app():
    return mock.Mock()


def test_flask_extension_init_self_app(mocked_flask_app):
    ext = JAC(mocked_flask_app)
    assert ext.app is mocked_flask_app


def test_flask_extension_jinja_env_add_extension(mocked_flask_app):
    ext = JAC()
    ext.init_app(mocked_flask_app)
    mocked_flask_app.jinja_env.add_extension.assert_called_once_with('jac.CompilerExtension')


def test_flask_extension_jinja_env_compressor_output_dir(mocked_flask_app):
    mocked_flask_app.static_folder = '/static/folder'
    mocked_flask_app.config = dict()

    ext = JAC()
    ext.init_app(mocked_flask_app)
    assert mocked_flask_app.jinja_env.compressor_output_dir == '/static/folder'


def test_flask_extension_jinja_env_static_prefix(mocked_flask_app):
    mocked_flask_app.static_url_path = '/static-url'
    mocked_flask_app.config = dict()

    ext = JAC()
    ext.init_app(mocked_flask_app)
    assert mocked_flask_app.jinja_env.compressor_static_prefix == '/static-url'


def test_flask_extension_jinja_env_source_dirs(mocked_flask_app):
    ext = JAC()
    ext.init_app(mocked_flask_app)
    mocked_flask_app.jinja_env.compressor_source_dirs == static_finder(mocked_flask_app)
