try:
    import cStringIO as StringIO
except ImportError:  # pragma: nocover
    import StringIO  # pragma: nocover

import mock
import pytest


class BaseCompilerTest:
    subprocess_package = None

    @pytest.fixture
    def stdin(self):
        return StringIO.StringIO()

    stdout = stdin

    @pytest.fixture
    def subprocess(self):
        return mock.patch(self.subprocess_package)
