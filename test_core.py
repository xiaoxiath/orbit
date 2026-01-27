"""Test core functionality without dependencies."""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def test_satellite_creation():
    """Test satellite creation without dependencies."""
    from orbit.core.satellite import Satellite, SatelliteParameter, SafetyLevel

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
        applescript_template='return "test"',
    )

    assert satellite.name == "test_satellite"
    assert satellite.safety_level == SafetyLevel.SAFE
    print("✅ Satellite creation test passed")

    # Test to_openai_function
    openai_func = satellite.to_openai_function()
    assert openai_func["type"] == "function"
    assert openai_func["function"]["name"] == "test_satellite"
    print("✅ OpenAI function export test passed")

    # Test to_dict
    satellite_dict = satellite.to_dict()
    assert satellite_dict["name"] == "test_satellite"
    assert satellite_dict["safety_level"] == "safe"
    print("✅ Dict export test passed")


def test_constellation():
    """Test constellation registry."""
    from orbit.core.satellite import Satellite, SafetyLevel
    from orbit.core.constellation import Constellation

    constellation = Constellation()

    # Create test satellite
    satellite1 = Satellite(
        name="test_satellite_1",
        description="Test satellite 1",
        category="test",
        parameters=[],
        safety_level=SafetyLevel.SAFE,
        applescript_template='return "test"',
    )

    satellite2 = Satellite(
        name="test_satellite_2",
        description="Test satellite 2",
        category="test",
        parameters=[],
        safety_level=SafetyLevel.MODERATE,
        applescript_template='return "test"',
    )

    # Register satellites
    constellation.register(satellite1)
    constellation.register(satellite2)

    # Test list_all
    all_satellites = constellation.list_all()
    assert len(all_satellites) == 2
    print("✅ Constellation register test passed")

    # Test get
    retrieved = constellation.get("test_satellite_1")
    assert retrieved is not None
    assert retrieved.name == "test_satellite_1"
    print("✅ Constellation get test passed")

    # Test list_by_category
    test_satellites = constellation.list_by_category("test")
    assert len(test_satellites) == 2
    print("✅ Constellation list_by_category test passed")

    # Test list_by_safety
    safe_satellites = constellation.list_by_safety(SafetyLevel.SAFE)
    assert len(safe_satellites) == 1
    print("✅ Constellation list_by_safety test passed")

    # Test stats
    stats = constellation.get_stats()
    assert stats["total_satellites"] == 2
    assert stats["categories"] == 1
    print("✅ Constellation stats test passed")


def test_parameter_validation():
    """Test parameter validation."""
    from orbit.core.satellite import Satellite, SatelliteParameter, SafetyLevel
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
            ),
            SatelliteParameter(
                name="enum_param",
                type="string",
                description="Enum parameter",
                required=True,
                enum=["a", "b", "c"]
            )
        ],
        safety_level=SafetyLevel.SAFE,
        applescript_template='return "test"',
    )

    # Test valid parameters
    satellite.validate_parameters({
        "required_param": "value",
        "enum_param": "a"
    })
    print("✅ Parameter validation (valid) test passed")

    # Test missing required parameter
    try:
        satellite.validate_parameters({})
        assert False, "Should have raised ParameterValidationError"
    except ParameterValidationError:
        print("✅ Parameter validation (missing required) test passed")

    # Test invalid enum value
    try:
        satellite.validate_parameters({
            "required_param": "value",
            "enum_param": "invalid"
        })
        assert False, "Should have raised ParameterValidationError"
    except ParameterValidationError:
        print("✅ Parameter validation (invalid enum) test passed")


def test_exceptions():
    """Test exception hierarchy."""
    from orbit.core.exceptions import (
        OrbitError,
        ShieldError,
        AppleScriptError,
        SatelliteNotFoundError,
    )

    # Test exception inheritance
    assert issubclass(ShieldError, OrbitError)
    assert issubclass(AppleScriptError, OrbitError)
    assert issubclass(SatelliteNotFoundError, OrbitError)
    print("✅ Exception hierarchy test passed")

    # Test AppleScriptError attributes
    error = AppleScriptError(
        message="Test error",
        script="tell application \"Finder\"\nreturn",
        return_code=1
    )
    assert error.script == 'tell application "Finder"\nreturn'
    assert error.return_code == 1
    print("✅ AppleScriptError attributes test passed")


def main():
    """Run all tests."""
    print("🛸 Orbit - Core Functionality Tests\n")
    print("=" * 60)

    try:
        test_satellite_creation()
        test_constellation()
        test_parameter_validation()
        test_exceptions()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("\n📊 Summary:")
        print("   - Satellite creation and export: ✓")
        print("   - Constellation registry: ✓")
        print("   - Parameter validation: ✓")
        print("   - Exception hierarchy: ✓")
        print("\n🚀 Core framework is working correctly!")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
