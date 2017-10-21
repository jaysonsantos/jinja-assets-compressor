import mock
import pytest
from six import StringIO


class BaseCompilerTest:
    subprocess_package = None

    @pytest.fixture
    def stdin(self):
        return StringIO.StringIO()

    stdout = stdin

    @pytest.fixture
    def subprocess(self):
        return mock.patch(self.subprocess_package)
