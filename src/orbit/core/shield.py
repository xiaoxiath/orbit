"""Safety shield - validates and controls mission execution."""

from typing import Dict, List, Optional, Callable
from pathlib import Path
from enum import Enum

from orbit.core.satellite import Satellite, SafetyLevel
from orbit.core.exceptions import ShieldError


class ShieldAction(Enum):
    """Shield action after safety check."""

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_CONFIRMATION = "require_confirmation"


class SafetyShield:
    """Safety shield - validates and controls mission execution."""

    # Default shield rules
    DEFAULT_RULES = {
        SafetyLevel.SAFE: ShieldAction.ALLOW,
        SafetyLevel.MODERATE: ShieldAction.REQUIRE_CONFIRMATION,
        SafetyLevel.DANGEROUS: ShieldAction.REQUIRE_CONFIRMATION,
        SafetyLevel.CRITICAL: ShieldAction.DENY,
    }

    # Protected paths (dangerous to modify)
    # Protected system paths (too broad paths like "/" are excluded)
    PROTECTED_PATHS = [
        Path("/System"),
        Path("/Library"),
        Path("/usr"),
        Path("/bin"),
        Path("/sbin"),
        Path("/etc"),
        Path("/var"),
    ]

    # Dangerous command patterns
    DANGEROUS_COMMANDS = [
        "rm -rf /",
        "dd if=/dev/zero",
        ":(){ :|:& };:",  # fork bomb
        "mkfs",
        "chmod 000",
        "chown root",
    ]

    def __init__(
        self,
        rules: Optional[Dict[SafetyLevel, ShieldAction]] = None,
        confirmation_callback: Optional[Callable[[Satellite, dict], bool]] = None,
        protected_paths: Optional[List[Path]] = None,
        dangerous_commands: Optional[List[str]] = None,
    ):
        """Initialize the safety shield.

        Args:
            rules: Safety level to action mapping
            confirmation_callback: User confirmation function
            protected_paths: List of protected system paths
            dangerous_commands: List of dangerous command patterns
        """
        self.rules = rules or self.DEFAULT_RULES
        self.confirmation_callback = confirmation_callback
        self.protected_paths = protected_paths or self.PROTECTED_PATHS
        self.dangerous_commands = dangerous_commands or self.DANGEROUS_COMMANDS

    def validate(self, satellite: Satellite, parameters: dict) -> bool:
        """Validate mission safety.

        Args:
            satellite: Satellite to validate
            parameters: Mission parameters

        Returns:
            True if safe

        Raises:
            ShieldError: If validation fails
        """
        action = self.rules.get(satellite.safety_level, ShieldAction.DENY)

        # Check protected paths
        if "path" in parameters:
            self._check_path(parameters["path"])

        # Check dangerous commands
        if "command" in parameters:
            self._check_command(parameters["command"])

        # Apply shield action
        if action == ShieldAction.DENY:
            raise ShieldError(
                f"Satellite '{satellite.name}' blocked due to {satellite.safety_level.value} safety level"
            )

        elif action == ShieldAction.REQUIRE_CONFIRMATION:
            if self.confirmation_callback:
                if not self.confirmation_callback(satellite, parameters):
                    raise ShieldError("User denied the mission")
            else:
                raise ShieldError(
                    f"Satellite '{satellite.name}' requires confirmation but no callback provided"
                )

        return True

    def _check_path(self, path: str) -> None:
        """Check if path is protected.

        Args:
            path: Path to check

        Raises:
            ShieldError: If path is protected
        """
        resolved_path = Path(path).expanduser().resolve()

        for protected in self.protected_paths:
            try:
                if resolved_path.is_relative_to(protected):
                    raise ShieldError(f"Protected path detected: {path}")
            except ValueError:
                # Different drives on Windows, not applicable for macOS
                pass

    def _check_command(self, command: str) -> None:
        """Check if command is dangerous.

        Args:
            command: Command to check

        Raises:
            ShieldError: If command is dangerous
        """
        for dangerous in self.dangerous_commands:
            if dangerous in command:
                raise ShieldError(f"Dangerous command detected: {command}")

    def add_protected_path(self, path: str) -> None:
        """Add a protected path.

        Args:
            path: Path string to protect
        """
        self.protected_paths.append(Path(path).expanduser().resolve())

    def remove_protected_path(self, path: str) -> None:
        """Remove a protected path.

        Args:
            path: Path string to unprotect
        """
        path_obj = Path(path).expanduser().resolve()
        if path_obj in self.protected_paths:
            self.protected_paths.remove(path_obj)
