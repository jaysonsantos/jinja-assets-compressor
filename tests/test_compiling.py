import pytest
import jac


class TestCompiling:
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
  border-color: $blue '''

    def test_compiling(self, sample_sass):
        compiled_css = """.content-navigation {
  border-color: #3bbfce;
  color: #2ca2af; }

.border {
  padding: 8px;
  margin: 8px;
  border-color: #3bbfce; }
"""

        assert jac.compile(sample_sass, 'text/sass') == compiled_css
