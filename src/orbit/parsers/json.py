"""Result parser base classes and implementations."""

from abc import ABC, abstractmethod
from typing import Any
import json
import re


class ResultParser(ABC):
    """Base result parser."""

    @abstractmethod
    def parse(self, raw_output: str) -> Any:
        """Parse raw AppleScript output.

        Args:
            raw_output: Raw output from AppleScript

        Returns:
            Parsed result
        """
        pass


class JSONResultParser(ResultParser):
    """Parse JSON output."""

    def parse(self, raw_output: str) -> dict:
        """Parse JSON output.

        Args:
            raw_output: JSON string

        Returns:
            Parsed dictionary

        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse JSON: {raw_output}")


class DelimitedResultParser(ResultParser):
    """Parse delimited output (e.g., 'value1|value2|value3')."""

    def __init__(self, delimiter: str = "|", field_names: list[str] = None):
        """Initialize parser.

        Args:
            delimiter: Delimiter character
            field_names: Optional field names for dict output
        """
        self.delimiter = delimiter
        self.field_names = field_names

    def parse(self, raw_output: str) -> dict | list:
        """Parse delimited output.

        Args:
            raw_output: Delimited string

        Returns:
            Dict if field_names provided, list otherwise
        """
        parts = raw_output.split(self.delimiter)
        if self.field_names:
            return dict(zip(self.field_names, parts))
        return parts


class RegexResultParser(ResultParser):
    """Parse output using regex patterns."""

    def __init__(self, pattern: str, group_names: list[str] = None):
        """Initialize parser.

        Args:
            pattern: Regex pattern
            group_names: Optional group names for dict output
        """
        self.pattern = re.compile(pattern)
        self.group_names = group_names

    def parse(self, raw_output: str) -> dict | list:
        """Parse output using regex.

        Args:
            raw_output: String to parse

        Returns:
            Dict if group_names provided, list otherwise

        Raises:
            ValueError: If pattern doesn't match
        """
        match = self.pattern.search(raw_output)
        if not match:
            raise ValueError(f"Regex pattern did not match: {raw_output}")

        groups = match.groups()
        if self.group_names:
            return dict(zip(self.group_names, groups))
        return groups


class BooleanResultParser(ResultParser):
    """Parse boolean output."""

    def parse(self, raw_output: str) -> bool:
        """Parse boolean output.

        Args:
            raw_output: String representing boolean

        Returns:
            Boolean value
        """
        return raw_output.strip().lower() in ("true", "yes", "1")
