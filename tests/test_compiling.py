import pytest

from jac.compressors.coffee import CoffeeScriptCompressor
from jac.compressors.less import LessCompressor
from jac.compressors.javascript import JavaScriptCompressor
from jac.compressors.sass import SassCompressor

class TestSass:
    @pytest.fixture
    def sample_sass(self):
        """
        Returns a simple SAAS script for testing
        """

        return '''$blue: #3bbfce
$margin: 16px

.content-navigation
  border-color: $blue
  color: darken($blue, 9%)

.border
  padding: $margin / 2
  margin: $margin / 2
  border-color: $blue'''

    def test_compiling(self, sample_sass):
        compiled_css = """.content-navigation {
  border-color: #3bbfce;
  color: #2ca2af; }

.border {
  padding: 8px;
  margin: 8px;
  border-color: #3bbfce; }
"""

        assert SassCompressor.compile(sample_sass, 'text/sass') == compiled_css


class TestLess:
    @pytest.fixture
    def sample_less(self):
        """
        Returns a simple LESS script for testing
        """

        return '''
            body {
              .test-class {
                color: #fff;
              }
            }
        '''

    def test_compiling(self, sample_less):
        compiled_css = 'body .test-class{color:#fff}'
        assert LessCompressor.compile(sample_less, 'text/less') == compiled_css


class TestCoffee:
    @pytest.fixture
    def sample_coffee(self):
        """
        Returns a simple coffee script for testing
        """

        return '''
foo = (str) ->
 alert str
 true

foo "Hello CoffeeScript!"
'''

    def test_compiling(self, sample_coffee):
        compiled_js = '\
(function(){var foo;foo=function(str){alert(str);return true;};\
foo("Hello CoffeeScript!");}).call(this);'
        assert CoffeeScriptCompressor.compile(sample_coffee, 'text/coffeescript') == compiled_js


class TestJavaScript:
    @pytest.fixture
    def sample_javascript(self):
        """
        Returns some simple JavaScript for testing
        """

        return '''
var foo = function(str) {
  alert(str);
  return true;
};

foo("Hello CoffeeScript!");
'''

    def test_compiling(self, sample_javascript):
        compiled_js = 'var foo=function(str){alert(str);return true;};foo("Hello CoffeeScript!");'
        assert JavaScriptCompressor.compile(sample_javascript, 'text/javascript') == compiled_js
