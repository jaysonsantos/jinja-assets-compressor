import pytest

import jinja2

from jac import CompilerExtension


class TestCompression:
    @pytest.fixture
    def env(self):
        return jinja2.Environment(extensions=[CompilerExtension])

    def test_compress(self, env):
        html = '''{% compress "css" %}
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
