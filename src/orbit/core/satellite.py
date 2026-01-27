"""Satellite base class and data structures."""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from enum import Enum

from orbit.core.exceptions import ParameterValidationError


class SafetyLevel(Enum):
    """Satellite safety classification.

    Levels:
        SAFE: Read-only operations, no side effects
        MODERATE: Create/modify operations
        DANGEROUS: Delete operations
        CRITICAL: System-level operations
    """

    SAFE = "safe"
    MODERATE = "moderate"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"


@dataclass
class SatelliteParameter:
    """Parameter definition for a satellite.

    Attributes:
        name: Parameter name
        type: Parameter type (string, integer, boolean, object, array)
        description: Parameter description
        required: Whether parameter is required
        default: Default value
        enum: Optional list of allowed values
    """

    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None
    enum: Optional[list] = None


@dataclass
class Satellite:
    """Base satellite (tool) class.

    A satellite represents a single automation tool that can be launched
    to perform a specific task on macOS.

    Attributes:
        name: Unique identifier (snake_case)
        description: LLM-readable description
        category: Category (system, files, notes, etc.)
        parameters: List of parameter definitions
        safety_level: Safety classification
        applescript_template: Jinja2 template for AppleScript
        result_parser: Optional result parser function
        examples: Optional list of usage examples
        version: Satellite version
        author: Satellite author
    """

    name: str
    description: str
    category: str
    parameters: list[SatelliteParameter]
    safety_level: SafetyLevel
    applescript_template: str
    result_parser: Optional[Callable] = None
    examples: list[dict] = field(default_factory=list)
    version: str = "1.0.0"
    author: str = ""

    def to_openai_function(self) -> dict:
        """Export to OpenAI Function Calling format.

        Returns:
            OpenAI Function format dict
        """
        properties = {
            param.name: {
                "type": param.type,
                "description": param.description,
            }
            for param in self.parameters
        }

        for param in self.parameters:
            if param.default is not None:
                properties[param.name]["default"] = param.default
            if param.enum:
                properties[param.name]["enum"] = param.enum

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": [p.name for p in self.parameters if p.required],
                },
            },
        }

    def to_dict(self) -> dict:
        """Export to dictionary format.

        Returns:
            Satellite data dict
        """
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "safety_level": self.safety_level.value,
            "version": self.version,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.type,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                }
                for p in self.parameters
            ],
            "examples": self.examples,
        }

    def validate_parameters(self, parameters: dict) -> bool:
        """Validate parameters against satellite definition.

        Args:
            parameters: Parameters to validate

        Returns:
            True if valid

        Raises:
            ParameterValidationError: If validation fails
        """
        # Check required parameters
        for param in self.parameters:
            if param.required and param.name not in parameters:
                raise ParameterValidationError(
                    f"Missing required parameter '{param.name}' for satellite '{self.name}'"
                )

        # Check enum values
        for param in self.parameters:
            if param.enum and param.name in parameters:
                value = parameters[param.name]
                if value not in param.enum:
                    raise ParameterValidationError(
                        f"Parameter '{param.name}' must be one of {param.enum}, got '{value}'"
                    )

        return True
