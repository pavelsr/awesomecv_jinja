"""
Custom exceptions for awesomecv-jinja.

Provides specific exception types for different error scenarios.
"""


class AwesomeCVJinjaError(Exception):
    """Base exception for all awesomecv-jinja errors."""
    pass


class TemplateNotFoundError(AwesomeCVJinjaError):
    """Raised when a template is not found."""
    pass


class DocumentTypeNotFoundError(AwesomeCVJinjaError):
    """Raised when a document type is not available for the template."""
    pass


class RenderError(AwesomeCVJinjaError):
    """Raised when rendering fails."""
    pass


class CompilationError(AwesomeCVJinjaError):
    """Raised when PDF compilation fails."""
    pass

