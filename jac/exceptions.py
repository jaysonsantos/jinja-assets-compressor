class OfflineGenerationError(Exception):
    """
    Offline compression generation related exceptions
    """
    pass


class TemplateDoesNotExist(Exception):
    """
    This exception is raised when a template does not exist.
    """
    pass


class TemplateSyntaxError(Exception):
    """
    This exception is raised when a template syntax error is encountered.
    """
    pass
