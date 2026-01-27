"""Satellite registry - manages the constellation of tools."""

from typing import Dict, List, Optional
import json

from orbit.core.satellite import Satellite, SafetyLevel


class Constellation:
    """Satellite registry - manages the constellation of tools."""

    def __init__(self):
        """Initialize the constellation."""
        self._satellites: Dict[str, Satellite] = {}
        self._categories: Dict[str, List[str]] = {}

    def register(self, satellite: Satellite) -> None:
        """Register a satellite.

        Args:
            satellite: Satellite to register

        Raises:
            ValueError: If satellite already registered
        """
        if satellite.name in self._satellites:
            raise ValueError(f"Satellite '{satellite.name}' already registered")

        self._satellites[satellite.name] = satellite

        # Update category index
        if satellite.category not in self._categories:
            self._categories[satellite.category] = []
        self._categories[satellite.category].append(satellite.name)

    def unregister(self, name: str) -> None:
        """Unregister a satellite.

        Args:
            name: Satellite name

        Raises:
            ValueError: If satellite not found
        """
        if name not in self._satellites:
            raise ValueError(f"Satellite '{name}' not found")

        satellite = self._satellites[name]
        self._categories[satellite.category].remove(name)
        del self._satellites[name]

    def get(self, name: str) -> Optional[Satellite]:
        """Get satellite by name.

        Args:
            name: Satellite name

        Returns:
            Satellite instance or None
        """
        return self._satellites.get(name)

    def list_all(self) -> List[Satellite]:
        """List all satellites.

        Returns:
            List of all satellites
        """
        return list(self._satellites.values())

    def list_by_category(self, category: str) -> List[Satellite]:
        """List satellites by category.

        Args:
            category: Category name

        Returns:
            List of satellites in category
        """
        satellite_names = self._categories.get(category, [])
        return [self._satellites[name] for name in satellite_names]

    def list_by_safety(self, safety_level: SafetyLevel) -> List[Satellite]:
        """List satellites by safety level.

        Args:
            safety_level: Safety level

        Returns:
            List of satellites with given safety level
        """
        return [s for s in self._satellites.values() if s.safety_level == safety_level]

    def search(self, query: str) -> List[Satellite]:
        """Search satellites by name or description.

        Args:
            query: Search query

        Returns:
            List of matching satellites
        """
        query = query.lower()
        return [
            s
            for s in self._satellites.values()
            if query in s.name.lower() or query in s.description.lower()
        ]

    def to_openai_functions(self) -> List[dict]:
        """Export all satellites to OpenAI Functions format.

        Returns:
            List of OpenAI Function dicts
        """
        return [satellite.to_openai_function() for satellite in self._satellites.values()]

    def to_json_schema(self) -> str:
        """Export all satellites as JSON Schema string.

        Returns:
            JSON Schema string
        """
        return json.dumps(
            [satellite.to_dict() for satellite in self._satellites.values()],
            indent=2,
            ensure_ascii=False,
        )

    def get_categories(self) -> List[str]:
        """Get all category names.

        Returns:
            List of category names
        """
        return list(self._categories.keys())

    def get_stats(self) -> dict:
        """Get constellation statistics.

        Returns:
            Dict with total_satellites, categories, by_safety
        """
        return {
            "total_satellites": len(self._satellites),
            "categories": len(self._categories),
            "by_safety": {
                level.value: len(self.list_by_safety(level)) for level in SafetyLevel
            },
        }
