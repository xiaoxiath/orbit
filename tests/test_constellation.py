"""Tests for Constellation class."""

import pytest
import json
from orbit.core import Constellation, Satellite, SafetyLevel


class TestConstellationInit:
    """Tests for Constellation initialization."""

    def test_constellation_init(self):
        """Test constellation initialization."""
        constellation = Constellation()

        assert constellation._satellites == {}
        assert constellation._categories == {}


class TestConstellationRegister:
    """Tests for satellite registration."""

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
        constellation = Constellation()
        constellation.register(sample_satellite)

        assert "test_sat" in constellation._satellites
        assert constellation._satellites["test_sat"] is sample_satellite
        assert "test" in constellation._categories
        assert "test_sat" in constellation._categories["test"]

    def test_register_multiple_satellites(self):
        """Test registering multiple satellites."""
        constellation = Constellation()

        satellites = []
        for i in range(5):
            satellite = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            satellites.append(satellite)
            constellation.register(satellite)

        assert len(constellation._satellites) == 5
        assert len(constellation._categories["test"]) == 5

    def test_register_duplicate_satellite(self, sample_satellite):
        """Test that registering duplicate satellite raises error."""
        constellation = Constellation()
        constellation.register(sample_satellite)

        with pytest.raises(ValueError) as exc_info:
            constellation.register(sample_satellite)

        assert "already registered" in str(exc_info.value).lower()

    def test_register_different_categories(self):
        """Test registering satellites in different categories."""
        constellation = Constellation()

        sat1 = Satellite(
            name="system_sat",
            description="System satellite",
            category="system",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        sat2 = Satellite(
            name="files_sat",
            description="Files satellite",
            category="files",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(sat1)
        constellation.register(sat2)

        assert "system" in constellation._categories
        assert "files" in constellation._categories
        assert len(constellation._categories) == 2


class TestConstellationUnregister:
    """Tests for satellite unregistration."""

    def test_unregister_satellite(self):
        """Test unregistering a satellite."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation = Constellation()
        constellation.register(satellite)
        assert "test_sat" in constellation._satellites

        constellation.unregister("test_sat")

        assert "test_sat" not in constellation._satellites
        assert "test_sat" not in constellation._categories["test"]

    def test_unregister_nonexistent_satellite(self):
        """Test unregistering non-existent satellite raises error."""
        constellation = Constellation()

        with pytest.raises(ValueError) as exc_info:
            constellation.unregister("nonexistent")

        assert "not found" in str(exc_info.value).lower()

    def test_unregister_last_in_category(self):
        """Test unregistering last satellite removes category."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="unique_category",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation = Constellation()
        constellation.register(satellite)
        assert "unique_category" in constellation._categories

        constellation.unregister("test_sat")

        # Category should be removed or empty
        category_sats = constellation._categories.get("unique_category", [])
        assert len(category_sats) == 0


class TestConstellationGet:
    """Tests for get method."""

    def test_get_existing_satellite(self):
        """Test getting existing satellite."""
        satellite = Satellite(
            name="test_sat",
            description="Test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation = Constellation()
        constellation.register(satellite)

        retrieved = constellation.get("test_sat")

        assert retrieved is satellite

    def test_get_nonexistent_satellite(self):
        """Test getting non-existent satellite returns None."""
        constellation = Constellation()

        result = constellation.get("nonexistent")

        assert result is None


class TestConstellationListAll:
    """Tests for list_all method."""

    def test_list_all_empty(self):
        """Test listing all satellites when empty."""
        constellation = Constellation()

        result = constellation.list_all()

        assert result == []

    def test_list_all_with_satellites(self):
        """Test listing all satellites."""
        constellation = Constellation()

        satellites = []
        for i in range(3):
            satellite = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            satellites.append(satellite)
            constellation.register(satellite)

        result = constellation.list_all()

        assert len(result) == 3
        assert set(result) == set(satellites)


class TestConstellationListByCategory:
    """Tests for list_by_category method."""

    def test_list_by_category_empty(self):
        """Test listing by category when no satellites."""
        constellation = Constellation()

        result = constellation.list_by_category("system")

        assert result == []

    def test_list_by_category_existing(self):
        """Test listing satellites by category."""
        constellation = Constellation()

        # Add satellites to different categories
        for i in range(2):
            satellite = Satellite(
                name=f"system_{i}",
                description=f"System {i}",
                category="system",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        for i in range(3):
            satellite = Satellite(
                name=f"files_{i}",
                description=f"Files {i}",
                category="files",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        system_sats = constellation.list_by_category("system")
        files_sats = constellation.list_by_category("files")

        assert len(system_sats) == 2
        assert len(files_sats) == 3
        assert all(s.category == "system" for s in system_sats)
        assert all(s.category == "files" for s in files_sats)


class TestConstellationListBySafety:
    """Tests for list_by_safety method."""

    def test_list_by_safety_all_levels(self):
        """Test listing satellites by all safety levels."""
        constellation = Constellation()

        # Add satellites with different safety levels
        for level in SafetyLevel:
            satellite = Satellite(
                name=f"{level.value}_sat",
                description=f"{level.value} satellite",
                category="test",
                parameters=[],
                safety_level=level,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        safe_sats = constellation.list_by_safety(SafetyLevel.SAFE)
        moderate_sats = constellation.list_by_safety(SafetyLevel.MODERATE)
        dangerous_sats = constellation.list_by_safety(SafetyLevel.DANGEROUS)
        critical_sats = constellation.list_by_safety(SafetyLevel.CRITICAL)

        assert len(safe_sats) == 1
        assert len(moderate_sats) == 1
        assert len(dangerous_sats) == 1
        assert len(critical_sats) == 1

        assert safe_sats[0].safety_level == SafetyLevel.SAFE
        assert moderate_sats[0].safety_level == SafetyLevel.MODERATE
        assert dangerous_sats[0].safety_level == SafetyLevel.DANGEROUS
        assert critical_sats[0].safety_level == SafetyLevel.CRITICAL

    def test_list_by_safety_empty(self):
        """Test listing by safety level when no satellites."""
        constellation = Constellation()

        result = constellation.list_by_safety(SafetyLevel.SAFE)

        assert result == []


class TestConstellationSearch:
    """Tests for search method."""

    def test_search_by_name(self):
        """Test searching satellites by name."""
        constellation = Constellation()

        satellites = [
            Satellite(
                name="system_get_info",
                description="Get system info",
                category="system",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ),
            Satellite(
                name="files_list",
                description="List files",
                category="files",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ),
        ]

        for sat in satellites:
            constellation.register(sat)

        # Search for "system"
        results = constellation.search("system")

        assert len(results) == 1
        assert results[0].name == "system_get_info"

    def test_search_by_description(self):
        """Test searching satellites by description."""
        constellation = Constellation()

        satellite = Satellite(
            name="test_sat",
            description="This satellite gets system information",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(satellite)

        results = constellation.search("information")

        assert len(results) == 1
        assert results[0].name == "test_sat"

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        constellation = Constellation()

        satellite = Satellite(
            name="System_Get_Info",
            description="System satellite",
            category="system",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(satellite)

        # Search with different case
        results_lower = constellation.search("system")
        results_upper = constellation.search("SYSTEM")
        results_mixed = constellation.search("SySteM")

        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1

    def test_search_no_results(self):
        """Test search with no matching results."""
        constellation = Constellation()

        satellite = Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(satellite)

        results = constellation.search("nonexistent")

        assert results == []

    def test_search_partial_match(self):
        """Test search with partial matches."""
        constellation = Constellation()

        satellites = [
            Satellite(
                name="system_get_info",
                description="Get system info",
                category="system",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ),
            Satellite(
                name="system_set_volume",
                description="Set system volume",
                category="system",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ),
            Satellite(
                name="files_list",
                description="List files",
                category="files",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ),
        ]

        for sat in satellites:
            constellation.register(sat)

        results = constellation.search("system")

        assert len(results) == 2
        assert all("system" in s.name.lower() for s in results)


class TestConstellationToOpenAIFunctions:
    """Tests for to_openai_functions method."""

    def test_to_openai_functions_empty(self):
        """Test exporting when no satellites registered."""
        constellation = Constellation()

        result = constellation.to_openai_functions()

        assert result == []

    def test_to_openai_functions(self):
        """Test exporting satellites to OpenAI Functions format."""
        constellation = Constellation()

        satellite = Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(satellite)

        result = constellation.to_openai_functions()

        assert len(result) == 1
        assert result[0]["type"] == "function"
        assert result[0]["function"]["name"] == "test_sat"
        assert result[0]["function"]["description"] == "Test satellite"

    def test_to_openai_functions_multiple(self):
        """Test exporting multiple satellites."""
        constellation = Constellation()

        for i in range(3):
            satellite = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        result = constellation.to_openai_functions()

        assert len(result) == 3
        for i, func in enumerate(result):
            assert func["function"]["name"] == f"sat_{i}"


class TestConstellationToJSONSchema:
    """Tests for to_json_schema method."""

    def test_to_json_schema_empty(self):
        """Test JSON schema export when empty."""
        constellation = Constellation()

        result = constellation.to_json_schema()

        parsed = json.loads(result)
        assert parsed == []

    def test_to_json_schema(self):
        """Test exporting satellites as JSON Schema."""
        constellation = Constellation()

        satellite = Satellite(
            name="test_sat",
            description="Test satellite",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        constellation.register(satellite)

        result = constellation.to_json_schema()

        # Should be valid JSON
        parsed = json.loads(result)
        assert isinstance(parsed, list)
        assert len(parsed) == 1
        assert parsed[0]["name"] == "test_sat"
        assert parsed[0]["safety_level"] == "safe"

    def test_to_json_schema_multiple(self):
        """Test JSON schema export with multiple satellites."""
        constellation = Constellation()

        for i in range(2):
            satellite = Satellite(
                name=f"sat_{i}",
                description=f"Satellite {i}",
                category="test",
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        result = constellation.to_json_schema()

        parsed = json.loads(result)
        assert len(parsed) == 2


class TestConstellationGetCategories:
    """Tests for get_categories method."""

    def test_get_categories_empty(self):
        """Test getting categories when none registered."""
        constellation = Constellation()

        result = constellation.get_categories()

        assert result == []

    def test_get_categories(self):
        """Test getting all category names."""
        constellation = Constellation()

        # Register satellites in different categories
        categories = ["system", "files", "notes", "calendar"]
        for category in categories:
            satellite = Satellite(
                name=f"{category}_sat",
                description=f"{category} satellite",
                category=category,
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            )
            constellation.register(satellite)

        result = constellation.get_categories()

        assert len(result) == len(categories)
        assert set(result) == set(categories)


class TestConstellationGetStats:
    """Tests for get_stats method."""

    def test_get_stats_empty(self):
        """Test getting stats when no satellites."""
        constellation = Constellation()

        stats = constellation.get_stats()

        assert stats["total_satellites"] == 0
        assert stats["categories"] == 0
        assert stats["by_safety"]["safe"] == 0
        assert stats["by_safety"]["moderate"] == 0
        assert stats["by_safety"]["dangerous"] == 0
        assert stats["by_safety"]["critical"] == 0

    def test_get_stats(self):
        """Test getting constellation statistics."""
        constellation = Constellation()

        # Add satellites with different safety levels
        constellation.register(Satellite(
            name="safe_1",
            description="Safe 1",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        ))

        constellation.register(Satellite(
            name="safe_2",
            description="Safe 2",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        ))

        constellation.register(Satellite(
            name="moderate_1",
            description="Moderate 1",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.MODERATE,
            applescript_template='return "test"',
        ))

        stats = constellation.get_stats()

        assert stats["total_satellites"] == 3
        assert stats["categories"] == 1
        assert stats["by_safety"]["safe"] == 2
        assert stats["by_safety"]["moderate"] == 1
        assert stats["by_safety"]["dangerous"] == 0
        assert stats["by_safety"]["critical"] == 0

    def test_get_stats_multiple_categories(self):
        """Test stats with multiple categories."""
        constellation = Constellation()

        for category in ["system", "files", "notes"]:
            constellation.register(Satellite(
                name=f"{category}_sat",
                description=f"{category} satellite",
                category=category,
                parameters=[],
                safety_level=SafetyLevel.SAFE,
                applescript_template='return "test"',
            ))

        stats = constellation.get_stats()

        assert stats["categories"] == 3
        assert stats["total_satellites"] == 3


class TestConstellationIntegration:
    """Integration tests for Constellation."""

    def test_full_lifecycle(self):
        """Test full satellite lifecycle."""
        constellation = Constellation()

        # Create satellite
        satellite = Satellite(
            name="lifecycle_sat",
            description="Lifecycle test",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        # Register
        constellation.register(satellite)
        assert constellation.get("lifecycle_sat") is satellite

        # List
        all_sats = constellation.list_all()
        assert len(all_sats) == 1

        # Search
        results = constellation.search("lifecycle")
        assert len(results) == 1

        # Export
        openai_funcs = constellation.to_openai_functions()
        assert len(openai_funcs) == 1

        # Stats
        stats = constellation.get_stats()
        assert stats["total_satellites"] == 1

        # Unregister
        constellation.unregister("lifecycle_sat")
        assert constellation.get("lifecycle_sat") is None
