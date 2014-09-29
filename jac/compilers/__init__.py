compilers = {}


class CompilerMeta(type):
    """
    Register a compiler and ensure that will only be one compiler
    by mimetype.
    """
    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        for m in attrs.get('supported_mimetypes', []):
            if m in compilers:
                raise RuntimeError('For now, just one compiler by mimetype')
            compilers[m] = cls

        return cls


def compile(what, mimetype, cwd=None, uri_cwd=None, debug=None):
    """
    Compile a given text based on mimetype.

    The text to compile must be provided as a Unicode object and this
    function must return the compiled text as a Unicode object.
    """

    try:
        compiler = compilers[mimetype.lower()]
    except KeyError:
        raise RuntimeError('Compiler for mimetype %s not found.' % mimetype)

    return compiler.compile(what, mimetype.lower(), cwd=cwd,
                            uri_cwd=uri_cwd, debug=debug)


from .css import CssCompiler
from .sass import SassCompiler
from .less import LessCompiler
from .javascript import JavaScriptCompiler
