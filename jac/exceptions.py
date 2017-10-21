class JACException(Exception):
    """
    Base exception class for all JAC related errors.
    """
    pass


class OfflineGenerationError(JACException):
    """
    Offline compression generation related exceptions
    """
    pass


class TemplateDoesNotExist(JACException):
    """
    This exception is raised when a template does not exist.
    """
    pass


class TemplateSyntaxError(JACException):
    """
    This exception is raised when a template syntax error is encountered.
    """
    pass


class InvalidCompressorError(JACException):
    """
    This exception is raised when a compressor is not setup correctly.
    """
    pass
