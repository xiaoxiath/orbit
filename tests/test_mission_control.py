"""Tests for MissionControl class."""

import pytest
from unittest.mock import patch, MagicMock
from orbit.core import MissionControl, Satellite, SafetyLevel, SafetyShield
from orbit.core.exceptions import SatelliteNotFoundError


class TestMissionControlInit:
    """Tests for MissionControl initialization."""

    def test_mission_control_init_default(self):
        """Test MissionControl initialization with defaults."""
        mission = MissionControl()

        assert mission.constellation is not None
        assert mission.safety_shield is not None
        assert mission.launcher is not None
        assert mission.launcher.safety_shield is mission.safety_shield

    def test_mission_control_init_custom_shield(self):
        """Test MissionControl initialization with custom shield."""
        custom_shield = SafetyShield()
        mission = MissionControl(safety_shield=custom_shield)

        assert mission.safety_shield is custom_shield
        assert mission.launcher.safety_shield is custom_shield

    def test_mission_control_init_custom_launcher(self):
        """Test MissionControl initialization with custom launcher."""
        from orbit.core import Launcher

        custom_launcher = Launcher()
        mission = MissionControl(launcher=custom_launcher)

        assert mission.launcher is custom_launcher


class TestMissionControlRegister:
    """Tests for satellite registration methods."""

    @pytest.fixture
    def sample_satellite(self):
        """Create a sample satellite."""
        return Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

    def test_register_single_satellite(self, sample_satellite):
        """Test registering a single satellite."""
        mission = MissionControl()
        mission.register(sample_satellite)

        retrieved = mission.constellation.get("test_sat")
        assert retrieved is sample_satellite

    def test_register_multiple_satellites(self):
        """Test registering multiple satellites individually."""
        mission = MissionControl()

        satellites = []
        for i in range(3):
            sat = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            satellites.append(sat)
            mission.register(sat)

        # Verify all are registered
        for i in range(3):
            retrieved = mission.constellation.get(f"sat_{i}")
            assert retrieved is satellites[i]

    def test_register_constellation(self):
        """Test registering multiple satellites at once."""
        mission = MissionControl()

        satellites = []
        for i in range(5):
            satellites.append(Satellite(
                name=f"batch_sat_{i}",
                description=f"Batch satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ))

        mission.register_constellation(satellites)

        # Verify all are registered
        for i in range(5):
            retrieved = mission.constellation.get(f"batch_sat_{i}")
            assert retrieved is not None

    def test_register_duplicate_satellite(self):
        """Test registering duplicate satellite raises error."""
        satellite = Satellite(
            name="duplicate_sat",
            description="Duplicate",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        mission = MissionControl()
        mission.register(satellite)

        # Should raise on duplicate
        with pytest.raises(ValueError):
            mission.register(satellite)


class TestMissionControlLaunch:
    """Tests for mission launch methods."""

    @pytest.fixture
    def mission_with_satellite(self):
        """Create a mission with a registered satellite."""
        from orbit.core import SatelliteParameter

        satellite = Satellite(
            name="test_sat",
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

        mission = MissionControl()
        mission.register(satellite)
        return mission

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_satellite_success(self, mock_run, mission_with_satellite):
        """Test successful satellite launch."""
        mock_result = MagicMock()
        mock_result.stdout = "test output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = mission_with_satellite.launch("test_sat", {"param1": "hello"})

        assert result == "test output"

    def test_launch_nonexistent_satellite(self, mission_with_satellite):
        """Test launching non-existent satellite raises error."""
        with pytest.raises(SatelliteNotFoundError) as exc_info:
            mission_with_satellite.launch("nonexistent_sat", {})

        assert "nonexistent_sat" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_with_bypass_shield(self, mock_run, mission_with_satellite):
        """Test launching with shield bypass."""
        mock_result = MagicMock()
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = mission_with_satellite.launch("test_sat", {"param1": "test"}, bypass_shield=True)

        assert result == "output"

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_shield_blocks(self, mock_run):
        """Test that shield can block launches."""
        from orbit.core import SatelliteParameter

        # Create a CRITICAL satellite
        satellite = Satellite(
            name="critical_sat",
            description="Critical satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.CRITICAL,
            applescript_template='return "critical"',
        )

        mission = MissionControl()
        mission.register(satellite)

        # Should be blocked by shield
        with pytest.raises(Exception):  # ShieldError
            mission.launch("critical_sat", {})


class TestMissionControlExport:
    """Tests for export methods."""

    def test_export_openai_functions_empty(self):
        """Test exporting when no satellites registered."""
        mission = MissionControl()

        functions = mission.export_openai_functions()

        assert functions == []

    def test_export_openai_functions(self):
        """Test exporting satellites to OpenAI Functions format."""
        mission = MissionControl()

        # Register multiple satellites
        for i in range(3):
            satellite = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            mission.register(satellite)

        functions = mission.export_openai_functions()

        assert len(functions) == 3
        for i, func in enumerate(functions):
            assert func["type"] == "function"
            assert func["function"]["name"] == f"sat_{i}"
            assert "description" in func["function"]

    def test_export_openai_functions_with_parameters(self):
        """Test exporting satellites with parameters."""
        from orbit.core import SatelliteParameter

        satellite = Satellite(
            name="param_sat",
            description="Satellite with params",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="param1",
                    type="string",
                    description="First parameter",
                    required=True
                ),
                SatelliteParameter(
                    name="param2",
                    type="integer",
                    description="Second parameter",
                    required=False,
                    default=42
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        mission = MissionControl()
        mission.register(satellite)

        functions = mission.export_openai_functions()

        assert len(functions) == 1
        func = functions[0]
        assert func["function"]["name"] == "param_sat"

        # Check parameters
        params = func["function"]["parameters"]
        assert "param1" in params["properties"]
        assert "param2" in params["properties"]
        assert "param1" in params["required"]
        assert "param2" not in params["required"]


class TestExecuteFunctionCall:
    """Tests for execute_function_call method."""

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_function_call_basic(self, mock_run):
        """Test executing OpenAI function call format."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "result"',
        )

        mission = MissionControl()
        mission.register(satellite)

        mock_result = MagicMock()
        mock_result.stdout = "result"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # OpenAI function call format
        function_call = {
            "name": "test_sat",
            "arguments": "{}"
        }

        result = mission.execute_function_call(function_call)

        assert result == "result"

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_function_call_with_arguments(self, mock_run):
        """Test executing function call with arguments."""
        from orbit.core import SatelliteParameter

        satellite = Satellite(
            name="param_sat",
            description="Test",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="message",
                    type="string",
                    description="Message",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "{{ message }}"',
        )

        mission = MissionControl()
        mission.register(satellite)

        mock_result = MagicMock()
        mock_result.stdout = "hello world"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Arguments as JSON string
        function_call = {
            "name": "param_sat",
            "arguments": '{"message": "hello world"}'
        }

        result = mission.execute_function_call(function_call)

        assert result == "hello world"

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_function_call_arguments_dict(self, mock_run):
        """Test executing function call with arguments as dict."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        mission = MissionControl()
        mission.register(satellite)

        mock_result = MagicMock()
        mock_result.stdout = "test"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Arguments as dict
        function_call = {
            "name": "test_sat",
            "arguments": {}
        }

        result = mission.execute_function_call(function_call)

        assert result == "test"

    def test_execute_function_call_nonexistent_satellite(self):
        """Test executing function call for non-existent satellite."""
        mission = MissionControl()

        function_call = {
            "name": "nonexistent_sat",
            "arguments": "{}"
        }

        with pytest.raises(SatelliteNotFoundError):
            mission.execute_function_call(function_call)

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_function_call_invalid_json(self, mock_run):
        """Test executing function call with invalid JSON arguments."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        mission = MissionControl()
        mission.register(satellite)

        mock_result = MagicMock()
        mock_result.stdout = "test"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Invalid JSON
        function_call = {
            "name": "test_sat",
            "arguments": "{invalid json}"
        }

        # Should raise JSON decode error
        with pytest.raises(Exception):
            mission.execute_function_call(function_call)


class TestMissionControlIntegration:
    """Integration tests for MissionControl."""

    @patch('orbit.core.launcher.subprocess.run')
    def test_full_workflow(self, mock_run):
        """Test complete workflow: register, export, execute."""
        mock_result = MagicMock()
        mock_result.stdout = "workflow result"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Create mission
        mission = MissionControl()

        # Register satellites
        satellites = []
        for i in range(3):
            satellites.append(Satellite(
                name=f"workflow_sat_{i}",
                description=f"Workflow satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ))

        mission.register_constellation(satellites)

        # Export
        functions = mission.export_openai_functions()
        assert len(functions) == 3

        # Execute
        result = mission.launch("workflow_sat_1", {})
        assert result == "workflow result"

    def test_mission_control_with_custom_shield_policies(self):
        """Test MissionControl with custom shield policies."""
        from orbit.core import ShieldAction

        # Custom rules: allow MODERATE without confirmation
        custom_rules = {
            SafetyLevel.SAFE: ShieldAction.ALLOW,
            SafetyLevel.MODERATE: ShieldAction.ALLOW,
            SafetyLevel.DANGEROUS: ShieldAction.DENY,
            SafetyLevel.CRITICAL: ShieldAction.DENY,
        }

        custom_shield = SafetyShield(rules=custom_rules)
        mission = MissionControl(safety_shield=custom_shield)

        # Verify shield is applied
        assert mission.safety_shield.rules == custom_rules
