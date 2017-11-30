import contextlib
import shutil
import tempfile


class TempDir(object):
    """Fancy tempdir with context to also support old python versions."""

    def __init__(self):
        self.name = tempfile.mkdtemp()

    def close(self):
        shutil.rmtree(self.name)

    @classmethod
    def with_context(cls):
        return contextlib.closing(cls())
