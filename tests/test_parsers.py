"""Tests for Result Parsers."""

import pytest
from orbit.parsers.json import (
    ResultParser,
    JSONResultParser,
    DelimitedResultParser,
    RegexResultParser,
    BooleanResultParser,
)


class TestResultParser:
    """Tests for ResultParser base class."""

    def test_result_parser_is_abstract(self):
        """Test that ResultParser cannot be instantiated."""
        with pytest.raises(TypeError):
            ResultParser()

    def test_result_parser_has_parse_method(self):
        """Test that ResultParser defines parse interface."""
        assert hasattr(ResultParser, 'parse')


class TestJSONResultParser:
    """Tests for JSONResultParser."""

    def test_parse_valid_json_object(self):
        """Test parsing valid JSON object."""
        parser = JSONResultParser()
        json_str = '{"name": "test", "value": 42}'

        result = parser.parse(json_str)

        assert isinstance(result, dict)
        assert result["name"] == "test"
        assert result["value"] == 42

    def test_parse_valid_json_array(self):
        """Test parsing valid JSON array."""
        parser = JSONResultParser()
        json_str = '[1, 2, 3, "test"]'

        result = parser.parse(json_str)

        assert isinstance(result, list)
        assert result[0] == 1
        assert result[3] == "test"

    def test_parse_nested_json(self):
        """Test parsing nested JSON structures."""
        parser = JSONResultParser()
        json_str = '{"user": {"name": "Alice", "age": 30}, "items": [1, 2, 3]}'

        result = parser.parse(json_str)

        assert result["user"]["name"] == "Alice"
        assert result["items"][0] == 1

    def test_parse_json_with_whitespace(self):
        """Test parsing JSON with extra whitespace."""
        parser = JSONResultParser()
        json_str = '  {  "key"  :  "value"  }  '

        result = parser.parse(json_str)

        assert result["key"] == "value"

    def test_parse_empty_json_object(self):
        """Test parsing empty JSON object."""
        parser = JSONResultParser()
        json_str = '{}'

        result = parser.parse(json_str)

        assert result == {}

    def test_parse_json_boolean(self):
        """Test parsing JSON boolean values."""
        parser = JSONResultParser()
        json_str = '{"flag": true, "enabled": false}'

        result = parser.parse(json_str)

        assert result["flag"] is True
        assert result["enabled"] is False

    def test_parse_json_null(self):
        """Test parsing JSON null value."""
        parser = JSONResultParser()
        json_str = '{"value": null}'

        result = parser.parse(json_str)

        assert result["value"] is None

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON raises error."""
        parser = JSONResultParser()
        invalid_json = '{invalid json}'

        with pytest.raises(ValueError) as exc_info:
            parser.parse(invalid_json)

        assert "Failed to parse JSON" in str(exc_info.value)

    def test_parse_malformed_json(self):
        """Test parsing malformed JSON raises error."""
        parser = JSONResultParser()
        malformed_json = '{"key": value}'  # Missing quotes

        with pytest.raises(ValueError):
            parser.parse(malformed_json)

    def test_parse_empty_string(self):
        """Test parsing empty string raises error."""
        parser = JSONResultParser()

        with pytest.raises(ValueError):
            parser.parse("")


class TestDelimitedResultParser:
    """Tests for DelimitedResultParser."""

    def test_parse_pipe_delimited_no_names(self):
        """Test parsing pipe-delimited string without field names."""
        parser = DelimitedResultParser(delimiter="|")
        input_str = "value1|value2|value3"

        result = parser.parse(input_str)

        assert isinstance(result, list)
        assert result == ["value1", "value2", "value3"]

    def test_parse_pipe_delimited_with_names(self):
        """Test parsing pipe-delimited string with field names."""
        parser = DelimitedResultParser(
            delimiter="|",
            field_names=["name", "age", "city"]
        )
        input_str = "Alice|30|New York"

        result = parser.parse(input_str)

        assert isinstance(result, dict)
        assert result["name"] == "Alice"
        assert result["age"] == "30"
        assert result["city"] == "New York"

    def test_parse_comma_delimited(self):
        """Test parsing comma-delimited string."""
        parser = DelimitedResultParser(delimiter=",")
        input_str = "apple,banana,cherry"

        result = parser.parse(input_str)

        assert result == ["apple", "banana", "cherry"]

    def test_parse_colon_delimited_with_names(self):
        """Test parsing colon-delimited string."""
        parser = DelimitedResultParser(
            delimiter=":",
            field_names=["key", "value"]
        )
        input_str = "username:john_doe"

        result = parser.parse(input_str)

        assert result["key"] == "username"
        assert result["value"] == "john_doe"

    def test_parse_default_delimiter(self):
        """Test parsing with default delimiter (|)."""
        parser = DelimitedResultParser()
        input_str = "a|b|c"

        result = parser.parse(input_str)

        assert result == ["a", "b", "c"]

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        parser = DelimitedResultParser(delimiter="|")
        input_str = ""

        result = parser.parse(input_str)

        assert result == [""]

    def test_parse_single_value(self):
        """Test parsing string with single value."""
        parser = DelimitedResultParser(delimiter="|")
        input_str = "single"

        result = parser.parse(input_str)

        assert result == ["single"]

    def test_parse_with_extra_delimiters(self):
        """Test parsing with consecutive delimiters."""
        parser = DelimitedResultParser(delimiter="|")
        input_str = "a||c"

        result = parser.parse(input_str)

        assert result == ["a", "", "c"]

    def test_parse_mismatched_field_count(self):
        """Test parsing when field count doesn't match data."""
        parser = DelimitedResultParser(
            delimiter="|",
            field_names=["name", "age"]  # 2 fields
        )
        input_str = "Alice|30|Extra"  # 3 values

        result = parser.parse(input_str)

        # Extra value should be ignored
        assert result["name"] == "Alice"
        assert result["age"] == "30"
        assert len(result) == 2

    def test_parse_fewer_fields_than_names(self):
        """Test parsing when fewer values than field names."""
        parser = DelimitedResultParser(
            delimiter="|",
            field_names=["a", "b", "c"]  # 3 fields
        )
        input_str = "x|y"  # 2 values

        result = parser.parse(input_str)

        # Missing field should have empty value or error
        # Current implementation: zip stops at shortest
        assert result == {"a": "x", "b": "y"}

    def test_parse_special_characters(self):
        """Test parsing string with special characters."""
        parser = DelimitedResultParser(delimiter="|")
        input_str = "hello world|test@example.com|123-456-7890"

        result = parser.parse(input_str)

        assert result[0] == "hello world"
        assert result[1] == "test@example.com"
        assert result[2] == "123-456-7890"


class TestRegexResultParser:
    """Tests for RegexResultParser."""

    def test_parse_simple_pattern_no_groups(self):
        """Test parsing with simple pattern."""
        parser = RegexResultParser(pattern=r'\d+')
        input_str = "The value is 42"

        result = parser.parse(input_str)

        # No groups, should return empty tuple or match result
        # Actually groups() returns empty tuple if no groups defined
        assert result == ()

    def test_parse_pattern_with_groups_no_names(self):
        """Test parsing pattern with groups but no names."""
        parser = RegexResultParser(pattern=r'(\d{4})-(\d{2})-(\d{2})')
        input_str = "Date: 2024-01-15"

        result = parser.parse(input_str)

        assert isinstance(result, tuple)
        assert result == ("2024", "01", "15")

    def test_parse_pattern_with_groups_and_names(self):
        """Test parsing pattern with groups and names."""
        parser = RegexResultParser(
            pattern=r'(\d{4})-(\d{2})-(\d{2})',
            group_names=["year", "month", "day"]
        )
        input_str = "Date: 2024-01-15"

        result = parser.parse(input_str)

        assert isinstance(result, dict)
        assert result["year"] == "2024"
        assert result["month"] == "01"
        assert result["day"] == "15"

    def test_parse_email_pattern(self):
        """Test parsing email with regex."""
        parser = RegexResultParser(
            pattern=r'(\w+)@(\w+\.\w+)',
            group_names=["username", "domain"]
        )
        input_str = "Contact: john.doe@example.com"

        result = parser.parse(input_str)

        assert result["username"] == "john.doe"
        assert result["domain"] == "example.com"

    def test_parse_phone_pattern(self):
        """Test parsing phone number with regex."""
        parser = RegexResultParser(
            pattern=r'\((\d{3})\) (\d{3})-(\d{4})',
            group_names=["area", "prefix", "line"]
        )
        input_str = "Phone: (555) 123-4567"

        result = parser.parse(input_str)

        assert result["area"] == "555"
        assert result["prefix"] == "123"
        assert result["line"] == "4567"

    def test_parse_pattern_no_match(self):
        """Test when pattern doesn't match."""
        parser = RegexResultParser(pattern=r'\d+')
        input_str = "No numbers here"

        with pytest.raises(ValueError) as exc_info:
            parser.parse(input_str)

        assert "did not match" in str(exc_info.value).lower()

    def test_parse_pattern_multiple_matches(self):
        """Test when pattern matches multiple times (uses first)."""
        parser = RegexResultParser(
            pattern=r'(\w+)',
            group_names=["word"]
        )
        input_str = "one two three"

        result = parser.parse(input_str)

        # Should return first match
        assert result["word"] == "one"

    def test_parse_pattern_optional_groups(self):
        """Test pattern with optional groups."""
        parser = RegexResultParser(
            pattern=r'Value: (\d+)(?: units)?',
            group_names=["value"]
        )
        input_str = "Value: 42"

        result = parser.parse(input_str)

        assert result["value"] == "42"

    def test_parse_pattern_escaped_characters(self):
        """Test pattern with escaped characters."""
        parser = RegexResultParser(
            pattern=r'path=(.+?)\.txt',
            group_names=["filename"]
        )
        input_str = "file path=/Users/test/document.txt"

        result = parser.parse(input_str)

        assert result["filename"] == "/Users/test/document"

    def test_parse_case_sensitive(self):
        """Test that regex is case-sensitive by default."""
        parser = RegexResultParser(pattern=r'[A-Z]+')
        input_str = "test ABC abc"

        result = parser.parse(input_str)

        assert result == ("ABC",)

    def test_parse_case_insensitive_pattern(self):
        """Test case-insensitive pattern."""
        parser = RegexResultParser(
            pattern=r'(?i)[a-z]+',
            group_names=["text"]
        )
        input_str = "TEST"

        result = parser.parse(input_str)

        assert result["text"] == "TEST"


class TestBooleanResultParser:
    """Tests for BooleanResultParser."""

    def test_parse_true_string(self):
        """Test parsing 'true' string."""
        parser = BooleanResultParser()

        result = parser.parse("true")

        assert result is True

    def test_parse_true_uppercase(self):
        """Test parsing 'TRUE' string."""
        parser = BooleanResultParser()

        result = parser.parse("TRUE")

        assert result is True

    def test_parse_true_mixed_case(self):
        """Test parsing 'True' string."""
        parser = BooleanResultParser()

        result = parser.parse("True")

        assert result is True

    def test_parse_yes_string(self):
        """Test parsing 'yes' string."""
        parser = BooleanResultParser()

        result = parser.parse("yes")

        assert result is True

    def test_parse_yes_uppercase(self):
        """Test parsing 'YES' string."""
        parser = BooleanResultParser()

        result = parser.parse("YES")

        assert result is True

    def test_parse_one_string(self):
        """Test parsing '1' string."""
        parser = BooleanResultParser()

        result = parser.parse("1")

        assert result is True

    def test_parse_false_string(self):
        """Test parsing 'false' string."""
        parser = BooleanResultParser()

        result = parser.parse("false")

        assert result is False

    def test_parse_no_string(self):
        """Test parsing 'no' string."""
        parser = BooleanResultParser()

        result = parser.parse("no")

        assert result is False

    def test_parse_zero_string(self):
        """Test parsing '0' string."""
        parser = BooleanResultParser()

        result = parser.parse("0")

        assert result is False

    def test_parse_arbitrary_string(self):
        """Test parsing arbitrary string returns False."""
        parser = BooleanResultParser()

        result = parser.parse("random text")

        assert result is False

    def test_parse_with_whitespace(self):
        """Test parsing with leading/trailing whitespace."""
        parser = BooleanResultParser()

        result = parser.parse("  true  ")

        assert result is True

        result = parser.parse("\n\tTRUE\t\n")

        assert result is True

    def test_parse_empty_string(self):
        """Test parsing empty string returns False."""
        parser = BooleanResultParser()

        result = parser.parse("")

        assert result is False


class TestParserIntegration:
    """Integration tests for parsers."""

    def test_json_parser_in_satellite(self):
        """Test JSON parser usage in satellite context."""
        from orbit.core import Satellite, SafetyLevel

        parser = JSONResultParser()
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return \'{"key": "value"}\'',
            result_parser=parser
        )

        # Simulate AppleScript output
        result = satellite.result_parser.parse('{"key": "value"}')
        assert result["key"] == "value"

    def test_delimited_parser_in_satellite(self):
        """Test delimited parser usage in satellite context."""
        from orbit.core import Satellite, SafetyLevel

        parser = DelimitedResultParser(
            delimiter="|",
            field_names=["name", "value"]
        )
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test|42"',
            result_parser=parser
        )

        result = satellite.result_parser.parse("test|42")
        assert result["name"] == "test"
        assert result["value"] == "42"

    def test_boolean_parser_in_satellite(self):
        """Test boolean parser usage in satellite context."""
        from orbit.core import Satellite, SafetyLevel

        parser = BooleanResultParser()
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "true"',
            result_parser=parser
        )

        result = satellite.result_parser.parse("true")
        assert result is True

    def test_lambda_parser(self):
        """Test using lambda function as parser."""
        from orbit.core import Satellite, SafetyLevel

        parser = lambda x: x.upper()
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
            result_parser=parser
        )

        result = satellite.result_parser("test")
        assert result == "TEST"
