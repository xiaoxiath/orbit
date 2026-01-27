"""Tests for Satellite class."""

import pytest
from orbit.core import Satellite, SatelliteParameter, SafetyLevel


class TestSatellite:
    """Tests for Satellite class."""

    def test_satellite_creation(self):
        """Test satellite creation."""
        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        assert satellite.name == "test_satellite"
        assert satellite.safety_level == SafetyLevel.SAFE
        assert satellite.category == "test"

    def test_satellite_to_openai_function(self):
        """Test converting satellite to OpenAI function format."""
        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="param1",
                    type="string",
                    description="Test parameter",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "{{ param1 }}"',
        )

        openai_func = satellite.to_openai_function()

        assert openai_func["type"] == "function"
        assert openai_func["function"]["name"] == "test_satellite"
        assert openai_func["function"]["description"] == "Test satellite"
        assert "param1" in openai_func["function"]["parameters"]["properties"]
        assert "param1" in openai_func["function"]["parameters"]["required"]

    def test_satellite_to_dict(self):
        """Test converting satellite to dictionary."""
        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
            version="2.0.0",
        )

        satellite_dict = satellite.to_dict()

        assert satellite_dict["name"] == "test_satellite"
        assert satellite_dict["safety_level"] == "safe"
        assert satellite_dict["version"] == "2.0.0"

    def test_validate_parameters_success(self):
        """Test parameter validation success."""
        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="required_param",
                    type="string",
                    description="Required parameter",
                    required=True
                ),
                SatelliteParameter(
                    name="optional_param",
                    type="string",
                    description="Optional parameter",
                    required=False,
                    default="default_value"
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        # Should not raise
        satellite.validate_parameters({"required_param": "value"})

    def test_validate_parameters_missing_required(self):
        """Test parameter validation with missing required parameter."""
        from orbit.core.exceptions import ParameterValidationError

        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="required_param",
                    type="string",
                    description="Required parameter",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        with pytest.raises(ParameterValidationError):
            satellite.validate_parameters({})

    def test_validate_parameters_enum_validation(self):
        """Test parameter validation with enum values."""
        from orbit.core.exceptions import ParameterValidationError

        satellite = Satellite(
            name="test_satellite",
            description="Test satellite",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="choice",
                    type="string",
                    description="Choice parameter",
                    required=True,
                    enum=["option1", "option2", "option3"]
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        # Valid value
        satellite.validate_parameters({"choice": "option1"})

        # Invalid value
        with pytest.raises(ParameterValidationError):
            satellite.validate_parameters({"choice": "invalid"})


class TestSatelliteParameter:
    """Tests for SatelliteParameter class."""

    def test_parameter_creation(self):
        """Test parameter creation."""
        param = SatelliteParameter(
            name="test_param",
            type="string",
            description="Test parameter",
            required=True,
        )

        assert param.name == "test_param"
        assert param.type == "string"
        assert param.required is True
        assert param.default is None

    def test_parameter_with_default(self):
        """Test parameter with default value."""
        param = SatelliteParameter(
            name="test_param",
            type="string",
            description="Test parameter",
            required=False,
            default="default_value",
        )

        assert param.required is False
        assert param.default == "default_value"

    def test_parameter_with_enum(self):
        """Test parameter with enum values."""
        param = SatelliteParameter(
            name="choice",
            type="string",
            description="Choice parameter",
            enum=["a", "b", "c"]
        )

        assert param.enum == ["a", "b", "c"]


class TestSafetyLevel:
    """Tests for SafetyLevel enum."""

    def test_safety_levels(self):
        """Test safety level values."""
        assert SafetyLevel.SAFE.value == "safe"
        assert SafetyLevel.MODERATE.value == "moderate"
        assert SafetyLevel.DANGEROUS.value == "dangerous"
        assert SafetyLevel.CRITICAL.value == "critical"
