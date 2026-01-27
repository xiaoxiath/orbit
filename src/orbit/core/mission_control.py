"""Mission Control - main entry point for Orbit."""

from typing import List, Optional, Any

try:
    from jinja2 import Template
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

from orbit.core.constellation import Constellation
from orbit.core.satellite import Satellite
from orbit.core.launcher import Launcher
from orbit.core.shield import SafetyShield, SafetyLevel
from orbit.core.exceptions import ShieldError, AppleScriptError


class MissionControl:
    """Mission Control - main entry point for Orbit.

    Manages satellite constellation and mission execution.
    """

    def __init__(
        self, safety_shield: Optional["SafetyShield"] = None, launcher: Optional["Launcher"] = None
    ):
        """Initialize Mission Control.

        Args:
            safety_shield: Optional safety shield. Defaults to shield with default rules.
            launcher: Optional launcher instance. Defaults to new Launcher instance.
        """
        self.constellation = Constellation()
        self.safety_shield = safety_shield or SafetyShield()
        self.launcher = launcher or Launcher(safety_shield=self.safety_shield)

    def register(self, satellite: Satellite) -> None:
        """Register a single satellite.

        Args:
            satellite: Satellite instance to register

        Raises:
            ValueError: If satellite already registered
        """
        self.constellation.register(satellite)

    def register_constellation(self, satellites: List[Satellite]) -> None:
        """Register multiple satellites at once.

        Args:
            satellites: List of satellites to register
        """
        for satellite in satellites:
            self.register(satellite)

    def launch(
        self, satellite_name: str, parameters: dict, bypass_shield: bool = False
    ) -> Any:
        """Launch a mission (execute a satellite).

        Args:
            satellite_name: Name of the satellite to launch
            parameters: Mission parameters dict
            bypass_shield: Skip safety checks (not recommended)

        Returns:
            Mission result (type depends on satellite)

        Raises:
            SatelliteNotFoundError: If satellite not found
            ShieldError: If safety check fails
            AppleScriptError: If script execution fails
        """
        satellite = self.constellation.get(satellite_name)
        if not satellite:
            from orbit.core.exceptions import SatelliteNotFoundError
            raise SatelliteNotFoundError(f"Satellite '{satellite_name}' not found")

        return self.launcher.launch(satellite, parameters, bypass_shield=bypass_shield)

    def export_openai_functions(self) -> List[dict]:
        """Export all registered satellites to OpenAI Functions format.

        Returns:
            List of OpenAI Function format dicts
        """
        return self.constellation.to_openai_functions()

    def execute_function_call(self, function_call: dict) -> Any:
        """Execute an OpenAI function call response.

        Args:
            function_call: OpenAI function_call dict from response

        Returns:
            Mission result
        """
        import json

        name = function_call.get("name")
        arguments_str = function_call.get("arguments", "{}")
        arguments = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str

        return self.launch(name, arguments)
