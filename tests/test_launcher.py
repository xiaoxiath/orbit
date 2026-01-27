"""Tests for Launcher class."""

import pytest
from unittest.mock import patch, MagicMock
from orbit.core import Launcher, Satellite, SafetyLevel
from orbit.core.exceptions import AppleScriptError, TemplateRenderingError


class TestLauncherInit:
    """Tests for Launcher initialization."""

    def test_launcher_init_default(self):
        """Test launcher initialization with defaults."""
        launcher = Launcher()

        assert launcher.timeout == 30
        assert launcher.retry_on_failure is False
        assert launcher.max_retries == 3
        assert launcher.safety_shield is None

    def test_launcher_init_with_params(self):
        """Test launcher initialization with parameters."""
        mock_shield = MagicMock()

        launcher = Launcher(
            safety_shield=mock_shield,
            timeout=60,
            retry_on_failure=True,
            max_retries=5
        )

        assert launcher.timeout == 60
        assert launcher.retry_on_failure is True
        assert launcher.max_retries == 5
        assert launcher.safety_shield is mock_shield


class TestLauncherLaunch:
    """Tests for Launcher.launch method."""

    @pytest.fixture
    def sample_satellite(self):
        """Create a sample satellite for testing."""
        return Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test result"',
        )

    @pytest.fixture
    def satellite_with_params(self):
        """Create a satellite with parameters."""
        from orbit.core import SatelliteParameter

        return Satellite(
            name="test_sat_with_params",
            description="Test satellite with params",
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

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_basic(self, mock_run, sample_satellite):
        """Test basic satellite launch."""
        # Mock subprocess result
        mock_result = MagicMock()
        mock_result.stdout = "test result"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher()
        result = launcher.launch(sample_satellite, {})

        assert result == "test result"
        mock_run.assert_called_once()

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_with_parameters(self, mock_run, satellite_with_params):
        """Test satellite launch with parameters."""
        mock_result = MagicMock()
        mock_result.stdout = "hello world"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher()
        result = launcher.launch(satellite_with_params, {"param1": "hello world"})

        assert result == "hello world"
        # Verify template was rendered
        called_script = mock_run.call_args[0][2]  # Third argument is the script
        assert "hello world" in called_script

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_with_shield_validation(self, mock_run, sample_satellite):
        """Test launch with shield validation."""
        mock_result = MagicMock()
        mock_result.stdout = "test result"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        mock_shield = MagicMock()
        launcher = Launcher(safety_shield=mock_shield)

        result = launcher.launch(sample_satellite, {})

        assert result == "test result"
        mock_shield.validate.assert_called_once_with(sample_satellite, {})

    def test_launch_bypass_shield(self, sample_satellite):
        """Test launching with shield bypass."""
        mock_shield = MagicMock()
        mock_shield.validate.side_effect = Exception("Should not be called")

        launcher = Launcher(safety_shield=mock_shield)

        with patch('orbit.core.launcher.subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "test result"
            mock_result.stderr = ""
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            result = launcher.launch(sample_satellite, {}, bypass_shield=True)

            assert result == "test result"
            mock_shield.validate.assert_not_called()

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_applescript_error(self, mock_run, sample_satellite):
        """Test launch with AppleScript execution error."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "AppleScript error"
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        launcher = Launcher()

        with pytest.raises(AppleScriptError) as exc_info:
            launcher.launch(sample_satellite, {})

        assert "AppleScript execution failed" in str(exc_info.value)
        assert exc_info.value.return_code == 1

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_with_result_parser(self, mock_run):
        """Test launch with result parser."""
        # Create satellite with result parser
        satellite = Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
            result_parser=lambda x: x.upper(),
        )

        mock_result = MagicMock()
        mock_result.stdout = "test"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher()
        result = launcher.launch(satellite, {})

        assert result == "TEST"

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_with_retry_on_failure(self, mock_run, sample_satellite):
        """Test launch with retry on failure."""
        # Fail first two times, succeed on third
        mock_result_success = MagicMock()
        mock_result_success.stdout = "test result"
        mock_result_success.stderr = ""
        mock_result_success.returncode = 0

        mock_result_fail = MagicMock()
        mock_result_fail.stdout = ""
        mock_result_fail.stderr = "Temporary error"
        mock_result_fail.returncode = 1

        mock_run.side_effect = [
            mock_result_fail,
            mock_result_fail,
            mock_result_success
        ]

        launcher = Launcher(retry_on_failure=True, max_retries=3)
        result = launcher.launch(sample_satellite, {})

        assert result == "test result"
        assert mock_run.call_count == 3

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_retry_exhausted(self, mock_run, sample_satellite):
        """Test launch when retries are exhausted."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Persistent error"
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        launcher = Launcher(retry_on_failure=True, max_retries=3)

        with pytest.raises(AppleScriptError):
            launcher.launch(sample_satellite, {})

        assert mock_run.call_count == 3

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_no_retry_without_flag(self, mock_run, sample_satellite):
        """Test launch doesn't retry when retry_on_failure is False."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Error"
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        launcher = Launcher(retry_on_failure=False, max_retries=3)

        with pytest.raises(AppleScriptError):
            launcher.launch(sample_satellite, {})

        # Should only be called once (no retry)
        assert mock_run.call_count == 1

    @patch('orbit.core.launcher.subprocess.run')
    def test_launch_timeout(self, mock_run, sample_satellite):
        """Test launch with timeout."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired("osascript", 30)

        launcher = Launcher(timeout=30)

        with pytest.raises(AppleScriptError) as exc_info:
            launcher.launch(sample_satellite, {})

        assert "timed out" in str(exc_info.value).lower()


class TestRenderTemplate:
    """Tests for _render_template method."""

    def test_render_template_simple_string(self):
        """Test template rendering with simple string format."""
        launcher = Launcher()
        template = "return '{{ param1 }}' & {{ param2 }}"
        params = {"param1": "hello", "param2": "42"}

        # This will use fallback formatting if Jinja2 is not available
        result = launcher._render_template(template, params)

        # Result should contain parameter values
        assert "hello" in result or "hello" in result.lower()

    def test_render_template_missing_param(self):
        """Test template rendering with missing parameter."""
        launcher = Launcher()
        template = "return '{{ missing_param }}'"
        params = {}

        with pytest.raises(TemplateRenderingError) as exc_info:
            launcher._render_template(template, params)

        assert "Missing parameter" in str(exc_info.value) or "rendering failed" in str(exc_info.value).lower()

    def test_render_template_complex(self):
        """Test template rendering with complex template."""
        launcher = Launcher()
        template = """
        set paramName to "{{ name }}"
        set paramPath to "{{ path }}"
        return paramName & "|" & paramPath
        """
        params = {"name": "Test", "path": "/tmp/test"}

        result = launcher._render_template(template, params)

        assert "Test" in result
        assert "/tmp/test" in result


class TestExecuteAppleScript:
    """Tests for _execute_applescript method."""

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_applescript_success(self, mock_run):
        """Test successful AppleScript execution."""
        mock_result = MagicMock()
        mock_result.stdout = "success output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher()
        result = launcher._execute_applescript('return "test"')

        assert result == "success output"
        mock_run.assert_called_once()

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_applescript_with_timeout(self, mock_run):
        """Test AppleScript execution with custom timeout."""
        mock_result = MagicMock()
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher(timeout=60)
        launcher._execute_applescript('return "test"')

        # Check that timeout was passed
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs['timeout'] == 60

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_applescript_error(self, mock_run):
        """Test AppleScript execution with error."""
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Script error: syntax error"
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        launcher = Launcher()

        with pytest.raises(AppleScriptError) as exc_info:
            launcher._execute_applescript('invalid script')

        assert "AppleScript execution failed" in str(exc_info.value)
        assert exc_info.value.script == 'invalid script'
        assert exc_info.value.return_code == 1

    @patch('orbit.core.launcher.subprocess.run')
    def test_execute_applescript_timeout_error(self, mock_run):
        """Test AppleScript execution timeout."""
        import subprocess

        mock_run.side_effect = subprocess.TimeoutExpired("osascript", 30)

        launcher = Launcher(timeout=30)

        with pytest.raises(AppleScriptError) as exc_info:
            launcher._execute_applescript('delay 100')

        assert "timed out" in str(exc_info.value).lower()


class TestLaunchAsync:
    """Tests for launch_async method."""

    @pytest.mark.asyncio
    @patch('orbit.core.launcher.subprocess.run')
    async def test_launch_async_basic(self, mock_run):
        """Test basic async launch."""
        from orbit.core import Satellite

        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "async result"',
        )

        mock_result = MagicMock()
        mock_result.stdout = "async result"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        launcher = Launcher()
        result = await launcher.launch_async(satellite, {})

        assert result == "async result"

    @pytest.mark.asyncio
    async def test_launch_async_with_parameters(self):
        """Test async launch with parameters."""
        from orbit.core import Satellite, SatelliteParameter

        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[
                SatelliteParameter(
                    name="param1",
                    type="string",
                    description="Test",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "{{ param1 }}"',
        )

        with patch('orbit.core.launcher.subprocess.run') as mock_run:
            mock_result = MagicMock()
            mock_result.stdout = "test value"
            mock_result.stderr = ""
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            launcher = Launcher()
            result = await launcher.launch_async(satellite, {"param1": "test value"})

            assert result == "test value"
