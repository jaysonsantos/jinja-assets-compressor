# -*- coding: utf-8 -*-

import hashlib
import os

import mock
import pytest

import jinja2

from jac.compat import u, open, utf8_encode


class TestCompression:
    @pytest.fixture
    def env(self, tmpdir):
        from jac import CompressorExtension
        env = jinja2.Environment(extensions=[CompressorExtension])
        env.compressor_output_dir = tmpdir
        env.compressor_static_prefix = '/static/dist'
        return env

    @pytest.fixture
    def html_css(self):
        return '''<style type="text/sass">
$blue: #3bbfce
$margin: 16px

.content-navigation
  border-color: $blue
  color: darken($blue, 9%)

.border
  padding: $margin / 2
  margin: $margin / 2
  border-color: $blue
</style>
<style type="text/css">
#main {
    color: black;
}
</style>
'''

    @pytest.fixture
    def html_js(self):
        return '''<script type="text/javascript">
alert("Hi");
</script>'''

    @pytest.fixture
    def html_template(self):
        return '{% compress "css" %}' + self.html_css() + '{% endcompress %}'

    def test_render(self, env, html_template):
        template = env.from_string(html_template)
        expected = '<link type="text/css" rel="stylesheet" href="/static/dist/734b0dec0b33781a9b57f86b1a5e02a3.css" />'

        assert expected == template.render()

    def test_compile(self, tmpdir, html_css):
        from jac import CompressorExtension
        ext = CompressorExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[]))

        assert ext._compress_block('css', mock.Mock(return_value=html_css)) == '<link type="text/css" rel="stylesheet" href="/static/734b0dec0b33781a9b57f86b1a5e02a3.css" />'

    def test_compile_js(self, tmpdir, html_js):
        from jac import CompressorExtension
        ext = CompressorExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[]))

        assert ext._compress_block('js', mock.Mock(return_value=html_js)) == '<script type="text/javascript" src="/static/0749ffbc6e886a3a01ee6e6c15efc779.js"></script>'

    def test_compile_file(self, tmpdir):
        from jac import CompressorExtension
        ext = CompressorExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[str(tmpdir)]))
        static_file = os.path.join(str(tmpdir), 'test.sass')

        with open(static_file, 'w', encoding='utf-8') as f:
            f.write('''$blue: #3bbfce
$margin: 16px

.content-navigation
  border-color: $blue
  color: darken($blue, 9%)

.border
  padding: $margin / 2
  margin: $margin / 2
  border-color: $blue''')

        html = '<link type="text/sass" rel="stylesheet" src="test.sass" />'
        stat = os.stat(static_file)
        expected_hash = hashlib.md5(utf8_encode(html))
        expected_hash.update(utf8_encode('{}-{}'.format(stat.st_size, stat.st_mtime)))

        assert ext._compress_block('css', mock.Mock(return_value=html)) == '<link type="text/css" rel="stylesheet" href="/static/{}.css" />'.format(expected_hash.hexdigest())

    def test_offline_compress(self, env):
        from jac import Compressor

        tmpdir = str(env.compressor_output_dir)

        env.compressor_offline_compress = True
        env.compressor_source_dirs = [tmpdir]
        env.compressor_follow_symlinks = True
        env.compressor_output_dir = os.path.join(tmpdir, 'static/dist')

        compressor = Compressor(environment=env)
        css = '<link type="text/css" rel="stylesheet" href="/static/test.css" />'

        with open(os.path.join(tmpdir, 'test.html'), 'w') as fh:
            fh.write('<html>{% compress "css" %}'+css+'{% endcompress %}</html>')

        os.makedirs(os.path.join(tmpdir, 'static'))
        with open(os.path.join(tmpdir, 'static/test.css'), 'w') as fh:
            fh.write('html { display: block; }')

        compressor.offline_compress(env)

        assert os.path.exists(os.path.join(tmpdir, 'static/dist')) == True
