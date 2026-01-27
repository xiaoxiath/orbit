"""Result parsers package."""

from orbit.parsers.json import JSONResultParser
from orbit.parsers.delimited import DelimitedResultParser
from orbit.parsers.regex import RegexResultParser
from orbit.parsers.boolean import BooleanResultParser

__all__ = [
    "JSONResultParser",
    "DelimitedResultParser",
    "RegexResultParser",
    "BooleanResultParser",
]
