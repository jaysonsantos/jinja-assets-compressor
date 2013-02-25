import mock
import pytest

import jinja2


class TestCompression:
    @pytest.fixture
    def env(self, tmpdir):
        from jac import CompilerExtension
        env = jinja2.Environment(extensions=[CompilerExtension])
        env.compressor_output_dir = tmpdir
        return env

    @pytest.fixture
    def html(self):
        return '''{% compress "css" %}
<link rel="stylesheet" type="text/sass">
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
{% endcompress %}'''

    def _test_compress(self, env, html):
        html = ''''''

        template = env.from_string(html)
        expected = '''<style type="text/css">.content-navigation {
  border-color: #3bbfce;
  color: #2ca2af; }

.border {
  padding: 8px;
  margin: 8px;
  border-color: #3bbfce; }

#main {
    color: black;
}
</style>'''

        assert expected == template.render()

    def test_compile(self, tmpdir, html):
        from jac import CompilerExtension
        ext = CompilerExtension(mock.Mock(compressor_output_dir=tmpdir))

        assert ext._compile('css', mock.Mock(return_value=html)) == '<link type="text/css" rel="stylesheet" src="0db3ca27a871892cdac8ca68b6278cf727375249bd0df743e2ce36439582976a.css" />'
