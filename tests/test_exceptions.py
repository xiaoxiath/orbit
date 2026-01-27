"""Tests for Orbit exception hierarchy."""

import pytest
from orbit.core.exceptions import (
    OrbitError,
    ShieldError,
    AppleScriptError,
    AppleScriptTimeoutError,
    AppleScriptPermissionError,
    AppleScriptSyntaxError,
    SatelliteNotFoundError,
    ParameterValidationError,
    TemplateRenderingError,
)


class TestOrbitError:
    """Tests for OrbitError base exception."""

    def test_orbit_error_is_exception(self):
        """Test that OrbitError is an Exception."""
        assert issubclass(OrbitError, Exception)

    def test_orbit_error_can_be_raised(self):
        """Test that OrbitError can be raised."""
        with pytest.raises(OrbitError):
            raise OrbitError("Test error")

    def test_orbit_error_message(self):
        """Test Orbit error message."""
        error = OrbitError("Test message")
        assert str(error) == "Test message"

    def test_orbit_error_catching(self):
        """Test catching OrbitError."""
        try:
            raise OrbitError("Test")
        except OrbitError as e:
            assert str(e) == "Test"
        except Exception:
            pytest.fail("Should have caught OrbitError")


class TestShieldError:
    """Tests for ShieldError."""

    def test_shield_error_inheritance(self):
        """Test ShieldError inherits from OrbitError."""
        assert issubclass(ShieldError, OrbitError)

    def test_shield_error_raised(self):
        """Test ShieldError can be raised."""
        with pytest.raises(ShieldError):
            raise ShieldError("Shield validation failed")

    def test_shield_error_catch_as_orbit_error(self):
        """Test ShieldError can be caught as OrbitError."""
        try:
            raise ShieldError("Test")
        except OrbitError as e:
            assert isinstance(e, ShieldError)
            assert str(e) == "Test"


class TestAppleScriptError:
    """Tests for AppleScriptError."""

    def test_applescript_error_inheritance(self):
        """Test AppleScriptError inherits from OrbitError."""
        assert issubclass(AppleScriptError, OrbitError)

    def test_applescript_error_basic(self):
        """Test AppleScriptError with message only."""
        error = AppleScriptError("Script failed")
        assert str(error) == "Script failed"
        assert error.script is None
        assert error.return_code is None

    def test_applescript_error_with_script(self):
        """Test AppleScriptError with script."""
        error = AppleScriptError(
            message="Script failed",
            script='tell application "Finder" to quit'
        )
        assert str(error) == "Script failed"
        assert error.script == 'tell application "Finder" to quit'
        assert error.return_code is None

    def test_applescript_error_with_return_code(self):
        """Test AppleScriptError with return code."""
        error = AppleScriptError(
            message="Script failed",
            return_code=1
        )
        assert str(error) == "Script failed"
        assert error.script is None
        assert error.return_code == 1

    def test_applescript_error_full(self):
        """Test AppleScriptError with all parameters."""
        error = AppleScriptError(
            message="Script execution failed",
            script='invalid script',
            return_code=1
        )
        assert str(error) == "Script execution failed"
        assert error.script == 'invalid script'
        assert error.return_code == 1

    def test_applescript_error_catch_as_orbit_error(self):
        """Test AppleScriptError can be caught as OrbitError."""
        try:
            raise AppleScriptError("Test")
        except OrbitError as e:
            assert isinstance(e, AppleScriptError)


class TestAppleScriptTimeoutError:
    """Tests for AppleScriptTimeoutError."""

    def test_timeout_inheritance(self):
        """Test timeout error inherits from AppleScriptError."""
        assert issubclass(AppleScriptTimeoutError, AppleScriptError)
        assert issubclass(AppleScriptTimeoutError, OrbitError)

    def test_timeout_raised(self):
        """Test timeout error can be raised."""
        with pytest.raises(AppleScriptTimeoutError):
            raise AppleScriptTimeoutError("Script timed out")

    def test_timeout_with_script(self):
        """Test timeout error with script attribute."""
        error = AppleScriptTimeoutError(
            message="Timed out",
            script='delay 1000',
            return_code=None
        )
        assert error.script == 'delay 1000'


class TestAppleScriptPermissionError:
    """Tests for AppleScriptPermissionError."""

    def test_permission_inheritance(self):
        """Test permission error inherits from AppleScriptError."""
        assert issubclass(AppleScriptPermissionError, AppleScriptError)

    def test_permission_raised(self):
        """Test permission error can be raised."""
        with pytest.raises(AppleScriptPermissionError):
            raise AppleScriptPermissionError("Insufficient permissions")


class TestAppleScriptSyntaxError:
    """Tests for AppleScriptSyntaxError."""

    def test_syntax_inheritance(self):
        """Test syntax error inherits from AppleScriptError."""
        assert issubclass(AppleScriptSyntaxError, AppleScriptError)

    def test_syntax_raised(self):
        """Test syntax error can be raised."""
        with pytest.raises(AppleScriptSyntaxError):
            raise AppleScriptSyntaxError("Syntax error in script")


class TestSatelliteNotFoundError:
    """Tests for SatelliteNotFoundError."""

    def test_satellite_not_found_inheritance(self):
        """Test SatelliteNotFoundError inherits from OrbitError."""
        assert issubclass(SatelliteNotFoundError, OrbitError)

    def test_satellite_not_found_raised(self):
        """Test SatelliteNotFoundError can be raised."""
        with pytest.raises(SatelliteNotFoundError):
            raise SatelliteNotFoundError("Satellite 'test' not found")

    def test_satellite_not_found_message(self):
        """Test SatelliteNotFoundError message."""
        error = SatelliteNotFoundError("Satellite 'nonexistent' not found")
        assert "not found" in str(error).lower()


class TestParameterValidationError:
    """Tests for ParameterValidationError."""

    def test_parameter_validation_inheritance(self):
        """Test ParameterValidationError inherits from OrbitError."""
        assert issubclass(ParameterValidationError, OrbitError)

    def test_parameter_validation_raised(self):
        """Test ParameterValidationError can be raised."""
        with pytest.raises(ParameterValidationError):
            raise ParameterValidationError("Invalid parameter")

    def test_parameter_validation_message(self):
        """Test ParameterValidationError message."""
        error = ParameterValidationError("Parameter 'name' is required")
        assert "parameter" in str(error).lower()


class TestTemplateRenderingError:
    """Tests for TemplateRenderingError."""

    def test_template_rendering_inheritance(self):
        """Test TemplateRenderingError inherits from OrbitError."""
        assert issubclass(TemplateRenderingError, OrbitError)

    def test_template_rendering_raised(self):
        """Test TemplateRenderingError can be raised."""
        with pytest.raises(TemplateRenderingError):
            raise TemplateRenderingError("Template rendering failed")

    def test_template_rendering_message(self):
        """Test TemplateRenderingError message."""
        error = TemplateRenderingError("Missing parameter: name")
        assert "template" in str(error).lower() or "parameter" in str(error).lower()


class TestExceptionHierarchy:
    """Tests for exception hierarchy structure."""

    def test_all_exceptions_inherit_from_orbit_error(self):
        """Test all custom exceptions inherit from OrbitError."""
        exceptions = [
            ShieldError,
            AppleScriptError,
            AppleScriptTimeoutError,
            AppleScriptPermissionError,
            AppleScriptSyntaxError,
            SatelliteNotFoundError,
            ParameterValidationError,
            TemplateRenderingError,
        ]

        for exc in exceptions:
            assert issubclass(exc, OrbitError), f"{exc.__name__} should inherit from OrbitError"

    def test_applescript_subtypes_inherit_correctly(self):
        """Test AppleScript subtypes inherit correctly."""
        assert issubclass(AppleScriptTimeoutError, AppleScriptError)
        assert issubclass(AppleScriptPermissionError, AppleScriptError)
        assert issubclass(AppleScriptSyntaxError, AppleScriptError)

    def test_exception_chaining(self):
        """Test exception can be chained."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise AppleScriptError("AppleScript failed") from e
        except AppleScriptError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)

    def test_catch_base_exception(self):
        """Test catching OrbitError catches all custom exceptions."""
        exceptions_to_test = [
            ShieldError("Test"),
            AppleScriptError("Test"),
            AppleScriptTimeoutError("Test"),
            AppleScriptPermissionError("Test"),
            AppleScriptSyntaxError("Test"),
            SatelliteNotFoundError("Test"),
            ParameterValidationError("Test"),
            TemplateRenderingError("Test"),
        ]

        for exc in exceptions_to_test:
            try:
                raise exc
            except OrbitError:
                pass  # Should catch all
            except Exception:
                pytest.fail(f"Should have caught {type(exc).__name__} as OrbitError")


class TestExceptionUsage:
    """Tests for exception usage patterns."""

    def test_raise_and_catch_specific(self):
        """Test raising and catching specific exception type."""
        with pytest.raises(AppleScriptError) as exc_info:
            raise AppleScriptTimeoutError("Timeout")

        assert isinstance(exc_info.value, AppleScriptTimeoutError)
        assert isinstance(exc_info.value, AppleScriptError)
        assert isinstance(exc_info.value, OrbitError)

    def test_exception_context(self):
        """Test exception with context."""
        try:
            raise ValueError("Context error")
        except ValueError as e:
            raise SatelliteNotFoundError("Not found") from e

    def test_multiple_exception_types(self):
        """Test differentiating between multiple exception types."""
        from orbit.core import Satellite, SatelliteParameter, SafetyLevel

        satellite = Satellite(
            name="test",
            description="Test",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="required_param",
                    type="string",
                    description="Required",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        # Test parameter validation error
        with pytest.raises(ParameterValidationError):
            satellite.validate_parameters({})

        # Test satellite not found
        constellation = __import__('orbit.core.constellation', fromlist=['Constellation']).Constellation()
        with pytest.raises(Exception):  # Will be caught as ValueError or custom
            constellation.get("nonexistent")  # Returns None, doesn't raise

    def test_exception_attributes(self):
        """Test exception attributes are preserved."""
        error = AppleScriptError(
            message="Test error",
            script='test script',
            return_code=42
        )

        assert error.script == 'test script'
        assert error.return_code == 42
        assert str(error) == "Test error"

    def test_exception_can_be_pickled(self):
        """Test exceptions can be pickled (for multiprocessing)."""
        import pickle

        error = AppleScriptError(
            message="Test",
            script='test',
            return_code=1
        )

        # Pickle and unpickle
        pickled = pickle.dumps(error)
        unpickled = pickle.loads(pickled)

        assert str(unpickled) == "Test"
        assert unpickled.script == 'test'
        assert unpickled.return_code == 1
