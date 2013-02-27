import os

import mock
import pytest

import jinja2


class TestCompression:
    @pytest.fixture
    def env(self, tmpdir):
        from jac import CompilerExtension
        env = jinja2.Environment(extensions=[CompilerExtension])
        env.compressor_output_dir = tmpdir
        env.compressor_static_prefix = '/static'
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
        expected = '<link type="text/css" rel="stylesheet" href="/static/c280e1cd5668088561df91a053f7ba19c1d4e333e2e4c5506748e2c2bc1b2fc7.css" />'

        assert expected == template.render()

    def test_compile(self, tmpdir, html_css):
        from jac import CompilerExtension
        ext = CompilerExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[]))

        assert ext._compile('css', mock.Mock(return_value=html_css)) == '<link type="text/css" rel="stylesheet" href="/static/c280e1cd5668088561df91a053f7ba19c1d4e333e2e4c5506748e2c2bc1b2fc7.css" />'

    def test_compile_js(self, tmpdir, html_js):
        from jac import CompilerExtension
        ext = CompilerExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[]))

        assert ext._compile('js', mock.Mock(return_value=html_js)) == '<script type="text/javascript" src="/static/adbdae2764f5a0ce68d02ca33b0b9d319e5b86675d1896b9f199ea0e88fb535a.js"></script>'

    def test_compile_file(self, tmpdir):
        from jac import CompilerExtension
        ext = CompilerExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static', compressor_source_dirs=[str(tmpdir)]))

        with open(os.path.join(str(tmpdir), 'test.sass'), 'wb') as f:
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

        assert ext._compile('css', mock.Mock(return_value=html)) == '<link type="text/css" rel="stylesheet" href="/static/331d363d3c3cbf5a22f29e190596f996d37e0777e7d3173240801236ee9eb8c7.css" />'
