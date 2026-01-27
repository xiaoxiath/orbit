"""Orbit exception hierarchy."""


class OrbitError(Exception):
    """Base exception for all Orbit errors."""

    pass


class ShieldError(OrbitError):
    """Shield safety check failed."""

    pass


class AppleScriptError(OrbitError):
    """AppleScript execution error."""

    def __init__(self, message: str, script: str = None, return_code: int = None):
        super().__init__(message)
        self.script = script
        self.return_code = return_code


class AppleScriptTimeoutError(AppleScriptError):
    """AppleScript execution timed out."""

    pass


class AppleScriptPermissionError(AppleScriptError):
    """AppleScript insufficient permissions."""

    pass


class AppleScriptSyntaxError(AppleScriptError):
    """AppleScript syntax error (template issue)."""

    pass


class SatelliteNotFoundError(OrbitError):
    """Satellite not found in constellation."""

    pass


class ParameterValidationError(OrbitError):
    """Parameter validation failed."""

    pass


class TemplateRenderingError(OrbitError):
    """Template rendering failed."""

    pass
