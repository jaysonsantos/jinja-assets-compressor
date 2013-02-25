compilers = {}


class CompilerMeta(type):
    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        for m in attrs['supported_mimetypes']:
            if m in compilers:
                raise RuntimeError('For now, just one compiler by mimetype')
            compilers[m] = cls

        return cls


def compile(what, mimetype=None):
    """
    Compile a given text.
    If mimetype is null, we assume what is a HTML tag and we try to get it's content and search for a compiler based on type attribute.
    If mimetype is not null, we just search for it's compiler and return compiled text.
    """
    if mimetype:
        try:
            compiler = compilers[mimetype.lower()]
        except KeyError:
            raise RuntimeError('Compiler for mimetype %s not found.' % mimetype)

        return compiler.compile(what)

    return what

from .sass import SassCompiler
