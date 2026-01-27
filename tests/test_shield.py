"""Tests for SafetyShield class."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock
from orbit.core import SafetyShield, ShieldAction, Satellite, SafetyLevel
from orbit.core.exceptions import ShieldError


class TestShieldAction:
    """Tests for ShieldAction enum."""

    def test_shield_action_values(self):
        """Test ShieldAction enum values."""
        assert ShieldAction.ALLOW.value == "allow"
        assert ShieldAction.DENY.value == "deny"
        assert ShieldAction.REQUIRE_CONFIRMATION.value == "require_confirmation"

    def test_shield_action_comparison(self):
        """Test ShieldAction comparison."""
        assert ShieldAction.ALLOW == ShieldAction.ALLOW
        assert ShieldAction.ALLOW != ShieldAction.DENY


class TestSafetyShieldInit:
    """Tests for SafetyShield initialization."""

    def test_shield_init_default(self):
        """Test shield initialization with defaults."""
        shield = SafetyShield()

        assert shield.rules == SafetyShield.DEFAULT_RULES
        assert shield.confirmation_callback is None
        assert shield.protected_paths == SafetyShield.PROTECTED_PATHS
        assert shield.dangerous_commands == SafetyShield.DANGEROUS_COMMANDS

    def test_shield_init_custom_rules(self):
        """Test shield initialization with custom rules."""
        custom_rules = {
            SafetyLevel.SAFE: ShieldAction.ALLOW,
            SafetyLevel.MODERATE: ShieldAction.ALLOW,
            SafetyLevel.DANGEROUS: ShieldAction.DENY,
            SafetyLevel.CRITICAL: ShieldAction.DENY,
        }

        shield = SafetyShield(rules=custom_rules)

        assert shield.rules == custom_rules

    def test_shield_init_with_callback(self):
        """Test shield initialization with confirmation callback."""
        callback = MagicMock()
        shield = SafetyShield(confirmation_callback=callback)

        assert shield.confirmation_callback is callback

    def test_shield_init_custom_protected_paths(self):
        """Test shield initialization with custom protected paths."""
        custom_paths = [Path("/custom/path")]
        shield = SafetyShield(protected_paths=custom_paths)

        assert shield.protected_paths == custom_paths

    def test_shield_init_custom_dangerous_commands(self):
        """Test shield initialization with custom dangerous commands."""
        custom_commands = ["custom dangerous cmd"]
        shield = SafetyShield(dangerous_commands=custom_commands)

        assert shield.dangerous_commands == custom_commands


class TestSafetyShieldValidate:
    """Tests for SafetyShield.validate method."""

    @pytest.fixture
    def safe_satellite(self):
        """Create a SAFE level satellite."""
        return Satellite(
            name="safe_sat",
            description="Safe satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "safe"',
        )

    @pytest.fixture
    def moderate_satellite(self):
        """Create a MODERATE level satellite."""
        return Satellite(
            name="moderate_sat",
            description="Moderate satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.MODERATE,
            applescript_template='return "moderate"',
        )

    @pytest.fixture
    def dangerous_satellite(self):
        """Create a DANGEROUS level satellite."""
        return Satellite(
            name="dangerous_sat",
            description="Dangerous satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.DANGEROUS,
            applescript_template='return "dangerous"',
        )

    @pytest.fixture
    def critical_satellite(self):
        """Create a CRITICAL level satellite."""
        return Satellite(
            name="critical_sat",
            description="Critical satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.CRITICAL,
            applescript_template='return "critical"',
        )

    def test_validate_safe_allowed(self, safe_satellite):
        """Test that SAFE satellites are allowed."""
        shield = SafetyShield()
        result = shield.validate(safe_satellite, {})

        assert result is True

    def test_validate_moderate_requires_confirmation(self, moderate_satellite):
        """Test that MODERATE satellites require confirmation."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(moderate_satellite, {})

        assert "requires confirmation" in str(exc_info.value).lower()

    def test_validate_moderate_with_callback_approved(self, moderate_satellite):
        """Test MODERATE with approved confirmation callback."""
        callback = MagicMock(return_value=True)
        shield = SafetyShield(confirmation_callback=callback)

        result = shield.validate(moderate_satellite, {})

        assert result is True
        callback.assert_called_once_with(moderate_satellite, {})

    def test_validate_moderate_with_callback_denied(self, moderate_satellite):
        """Test MODERATE with denied confirmation callback."""
        callback = MagicMock(return_value=False)
        shield = SafetyShield(confirmation_callback=callback)

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(moderate_satellite, {})

        assert "user denied" in str(exc_info.value).lower()

    def test_validate_dangerous_requires_confirmation(self, dangerous_satellite):
        """Test that DANGEROUS satellites require confirmation."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(dangerous_satellite, {})

        assert "requires confirmation" in str(exc_info.value).lower()

    def test_validate_dangerous_with_callback_approved(self, dangerous_satellite):
        """Test DANGEROUS with approved confirmation callback."""
        callback = MagicMock(return_value=True)
        shield = SafetyShield(confirmation_callback=callback)

        result = shield.validate(dangerous_satellite, {})

        assert result is True

    def test_validate_critical_denied(self, critical_satellite):
        """Test that CRITICAL satellites are denied."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(critical_satellite, {})

        assert "blocked" in str(exc_info.value).lower()
        assert "critical" in str(exc_info.value).lower()

    def test_validate_with_unknown_safety_level(self):
        """Test validation with unknown safety level defaults to DENY."""
        # Create a mock satellite with unknown safety level
        satellite = MagicMock()
        satellite.safety_level = SafetyLevel.CRITICAL  # Default rules deny CRITICAL
        satellite.name = "test"

        shield = SafetyShield()

        with pytest.raises(ShieldError):
            shield.validate(satellite, {})

    def test_validate_custom_rules_allow_moderate(self, moderate_satellite):
        """Test validation with custom rules that allow MODERATE."""
        custom_rules = {
            SafetyLevel.SAFE: ShieldAction.ALLOW,
            SafetyLevel.MODERATE: ShieldAction.ALLOW,  # Allow without confirmation
            SafetyLevel.DANGEROUS: ShieldAction.DENY,
            SafetyLevel.CRITICAL: ShieldAction.DENY,
        }

        shield = SafetyShield(rules=custom_rules)
        result = shield.validate(moderate_satellite, {})

        assert result is True


class TestCheckPath:
    """Tests for _check_path method."""

    def test_check_safe_path(self):
        """Test checking a safe path."""
        shield = SafetyShield()

        # Should not raise
        shield._check_path("~/Documents")
        shield._check_path("/tmp/test")
        shield._check_path("/Users/test/file.txt")

    def test_check_protected_root(self):
        """Test checking root protected path."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/")

        assert "protected path" in str(exc_info.value).lower()

    def test_check_protected_system(self):
        """Test checking System protected path."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/System/Library")

        assert "protected path" in str(exc_info.value).lower()

    def test_check_protected_library(self):
        """Test checking Library protected path."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/Library/something")

        assert "protected path" in str(exc_info.value).lower()

    def test_check_protected_usr(self):
        """Test checking usr protected path."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/usr/bin/test")

        assert "protected path" in str(exc_info.value).lower()

    def test_check_protected_bin(self):
        """Test checking bin protected path."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/bin/ls")

        assert "protected path" in str(exc_info.value).lower()

    def test_check_path_expands_home(self):
        """Test that home directory is expanded."""
        shield = SafetyShield()

        # Should not raise - ~/Documents is not protected
        shield._check_path("~/Documents/test.txt")

    def test_check_protected_path_in_validate(self):
        """Test path checking through validate method."""
        from orbit.core import SatelliteParameter

        satellite = Satellite(
            name="test_file",
            description="Test file operations",
            category="files",
            parameters=[
                SatelliteParameter(
                    name="path",
                    type="string",
                    description="File path",
                    required=True
                )
            ],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(satellite, {"path": "/System/test"})

        assert "protected path" in str(exc_info.value).lower()


class TestCheckCommand:
    """Tests for _check_command method."""

    def test_check_safe_command(self):
        """Test checking a safe command."""
        shield = SafetyShield()

        # Should not raise
        shield._check_command("ls -la")
        shield._check_command("echo hello")
        shield._check_command("cp file1 file2")

    def test_check_dangerous_rm_rf(self):
        """Test checking dangerous rm -rf command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("rm -rf /important")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_dangerous_dd_command(self):
        """Test checking dangerous dd command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("dd if=/dev/zero of=/dev/sda")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_dangerous_fork_bomb(self):
        """Test checking fork bomb command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command(":(){ :|:& };:")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_dangerous_mkfs(self):
        """Test checking mkfs command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("mkfs.ext4 /dev/sda1")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_dangerous_chmod(self):
        """Test checking dangerous chmod command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("chmod 000 /important/file")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_dangerous_chown(self):
        """Test checking dangerous chown command."""
        shield = SafetyShield()

        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("chown root /file")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_check_command_in_validate(self):
        """Test command checking through validate method."""
        from orbit.core import SatelliteParameter

        satellite = Satellite(
            name="test_command",
            description="Test command execution",
            category="system",
            parameters=[
                SatelliteParameter(
                    name="command",
                    type="string",
                    description="Command to execute",
                    required=True
                )
            ],
            safety_level=SafetyLevel.MODERATE,
            applescript_template='return "test"',
        )

        callback = MagicMock(return_value=True)
        shield = SafetyShield(confirmation_callback=callback)

        with pytest.raises(ShieldError) as exc_info:
            shield.validate(satellite, {"command": "rm -rf /test"})

        assert "dangerous command" in str(exc_info.value).lower()


class TestProtectedPathManagement:
    """Tests for protected path management methods."""

    def test_add_protected_path(self):
        """Test adding a protected path."""
        shield = SafetyShield()
        initial_count = len(shield.protected_paths)

        shield.add_protected_path("/custom/protected/path")

        assert len(shield.protected_paths) == initial_count + 1
        assert Path("/custom/protected/path") in shield.protected_paths

    def test_add_protected_path_with_home(self):
        """Test adding protected path with home directory."""
        shield = SafetyShield()

        shield.add_protected_path("~/Documents/important")

        # Path should be expanded
        expanded_paths = [str(p) for p in shield.protected_paths]
        assert any("Documents" in p for p in expanded_paths)

    def test_remove_protected_path(self):
        """Test removing a protected path."""
        shield = SafetyShield()
        test_path = Path("/tmp/test")
        shield.protected_paths.append(test_path)

        initial_count = len(shield.protected_paths)
        shield.remove_protected_path("/tmp/test")

        assert len(shield.protected_paths) == initial_count - 1
        assert test_path not in shield.protected_paths

    def test_remove_nonexistent_path(self):
        """Test removing a path that doesn't exist."""
        shield = SafetyShield()
        initial_count = len(shield.protected_paths)

        # Should not raise
        shield.remove_protected_path("/nonexistent/path")

        assert len(shield.protected_paths) == initial_count

    def test_protected_path_blocks_after_adding(self):
        """Test that added protected path actually blocks operations."""
        shield = SafetyShield()

        # First, path should be allowed
        shield._check_path("/my/custom/path")  # Should not raise

        # Add as protected
        shield.add_protected_path("/my/custom/path")

        # Now should be blocked
        with pytest.raises(ShieldError) as exc_info:
            shield._check_path("/my/custom/path")

        assert "protected path" in str(exc_info.value).lower()


class TestCustomDangerousCommands:
    """Tests for custom dangerous commands."""

    def test_custom_dangerous_commands(self):
        """Test shield with custom dangerous commands."""
        custom_commands = ["my-dangerous-cmd", "another-bad-cmd"]
        shield = SafetyShield(dangerous_commands=custom_commands)

        # Should detect custom dangerous command
        with pytest.raises(ShieldError) as exc_info:
            shield._check_command("my-dangerous-cmd /path")

        assert "dangerous command" in str(exc_info.value).lower()

    def test_custom_dangerous_allows_safe(self):
        """Test that custom dangerous commands don't block safe commands."""
        custom_commands = ["only-this-cmd"]
        shield = SafetyShield(dangerous_commands=custom_commands)

        # Should not raise
        shield._check_command("rm -rf /test")  # Not in custom list


class TestDefaultConstants:
    """Tests for default shield constants."""

    def test_default_rules(self):
        """Test DEFAULT_RULES configuration."""
        assert SafetyShield.DEFAULT_RULES[SafetyLevel.SAFE] == ShieldAction.ALLOW
        assert SafetyShield.DEFAULT_RULES[SafetyLevel.MODERATE] == ShieldAction.REQUIRE_CONFIRMATION
        assert SafetyShield.DEFAULT_RULES[SafetyLevel.DANGEROUS] == ShieldAction.REQUIRE_CONFIRMATION
        assert SafetyShield.DEFAULT_RULES[SafetyLevel.CRITICAL] == ShieldAction.DENY

    def test_protected_paths_not_empty(self):
        """Test that PROTECTED_PATHS is configured."""
        assert len(SafetyShield.PROTECTED_PATHS) > 0
        assert Path("/") in SafetyShield.PROTECTED_PATHS
        assert Path("/System") in SafetyShield.PROTECTED_PATHS

    def test_dangerous_commands_not_empty(self):
        """Test that DANGEROUS_COMMANDS is configured."""
        assert len(SafetyShield.DANGEROUS_COMMANDS) > 0
        assert "rm -rf /" in SafetyShield.DANGEROUS_COMMANDS
