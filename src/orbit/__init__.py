"""
Orbit - macOS Automation Toolkit

Put macOS automation in orbit 🛸
"""

__version__ = "0.1.0"
__author__ = "xiaoxiath"
__email__ = "tang123hao@gmail.com"

from orbit.core.mission_control import MissionControl
from orbit.core.satellite import Satellite, SatelliteParameter, SafetyLevel
from orbit.core.constellation import Constellation
from orbit.core.launcher import Launcher
from orbit.core.shield import SafetyShield, ShieldAction
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

__all__ = [
    # Main interface
    "MissionControl",
    # Core classes
    "Satellite",
    "SatelliteParameter",
    "SafetyLevel",
    "Constellation",
    "Launcher",
    "SafetyShield",
    "ShieldAction",
    # Exceptions
    "OrbitError",
    "ShieldError",
    "AppleScriptError",
    "AppleScriptTimeoutError",
    "AppleScriptPermissionError",
    "AppleScriptSyntaxError",
    "SatelliteNotFoundError",
    "ParameterValidationError",
    "TemplateRenderingError",
]
