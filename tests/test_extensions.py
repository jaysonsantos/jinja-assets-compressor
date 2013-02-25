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
    def html(self):
        return '''<link rel="stylesheet" type="text/sass">
$blue: #3bbfce
$margin: 16px

.content-navigation
  border-color: $blue
  color: darken($blue, 9%)

.border
  padding: $margin / 2
  margin: $margin / 2
  border-color: $blue
</link>
<style type="text/css">
#main {
    color: black;
}
</style>
'''

    @pytest.fixture
    def html_template(self):
        return '{% compress "css" %}' + self.html() + '{% endcompress %}'

    def test_render(self, env, html_template):
        template = env.from_string(html_template)
        expected = '<link type="text/css" rel="stylesheet" src="/static/761b879c0b499a9d7e48a152fa5aa91efb66ee2455e025e673fd9001ab27ca73.css" />'

        assert expected == template.render()

    def test_compile(self, tmpdir, html):
        from jac import CompilerExtension
        ext = CompilerExtension(mock.Mock(compressor_output_dir=tmpdir, compressor_static_prefix='/static'))

        assert ext._compile('css', mock.Mock(return_value=html)) == '<link type="text/css" rel="stylesheet" src="/static/761b879c0b499a9d7e48a152fa5aa91efb66ee2455e025e673fd9001ab27ca73.css" />'
