# Contributing to Orbit

> **Version:** 1.0.0
> **Last Updated:** 2026-01-27

Thank you for your interest in contributing to Orbit! This document provides guidelines and instructions for contributing to the project.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and considerate
- Use welcoming and inclusive language
- Be constructive in feedback
- Focus on what is best for the community

### Reporting Issues

If you encounter any issues or have concerns, please contact us at:
- GitHub Issues: https://github.com/xiaoxiath/orbit/issues
- Email: support@orbit.dev

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- macOS 12.0+ (for testing)
- Git
- Poetry (for dependency management)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/xiaoxiath/orbit.git
cd orbit

# Install dependencies
poetry install --with dev

# Activate virtual environment
poetry shell

# Run tests
pytest

# Run linting
ruff check .
black --check .
```

### Recommended Tools

- **IDE**: VS Code, PyCharm, or any Python IDE with type hints support
- **Git Client**: GitHub Desktop, SourceTree, or command line
- **Testing**: pytest with coverage reporting

---

## Development Workflow

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/orbit.git
cd orbit
```

### 2. Create Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Branch Naming Convention

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 3. Make Changes

Edit code following our coding standards (see below).

### 4. Test Changes

```bash
# Run all tests
pytest

# Run specific test
pytest tests/core/test_satellite.py

# Run with coverage
pytest --cov=orbit --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new satellite for X"
```

### Commit Message Format

Follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

**Example:**
```
feat(notes): add notes_search satellite

Implement a new satellite for searching notes in Apple Notes.
The satellite supports searching by title and body content.

Closes #123
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Coding Standards

### Python Style Guide

Follow PEP 8 with our modifications:

```python
# Good
from orbit import MissionControl
from orbit.core import Satellite, SafetyLevel


def launch_mission(satellite_name: str, parameters: dict) -> Any:
    """Launch a mission with the given satellite.

    Args:
        satellite_name: Name of the satellite to launch
        parameters: Mission parameters

    Returns:
        Mission result

    Raises:
        SatelliteNotFoundError: If satellite not found
    """
    mission = MissionControl()
    return mission.launch(satellite_name, parameters)
```

### Type Hints

All functions must have type hints:

```python
from typing import Optional, List, Dict, Any


def process_result(
    data: Dict[str, Any],
    parser: Optional[Callable] = None
) -> List[str]:
    ...
```

### Docstrings

Use Google style docstrings:

```python
def satellite_function(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: If param1 is invalid
    """
    pass
```

### Naming Conventions

- **Modules**: `lowercase_with_underscores`
- **Classes**: `CapitalizedWords`
- **Functions/Methods**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`

---

## Testing Guidelines

### Test Structure

```python
# tests/satellites/test_notes.py
import pytest
from orbit.satellites.notes import create
from orbit.core import SafetyLevel


class TestNotesCreate:
    """Tests for notes_create satellite."""

    def test_launch_creates_note(self):
        """Test that launching creates a note."""
        satellite = create.notes_create
        assert satellite.name == "notes_create"
        assert satellite.safety_level == SafetyLevel.MODERATE

    def test_launch_with_title_only(self):
        """Test launching with only title parameter."""
        # Test implementation
        pass

    @pytest.mark.integration
    def test_integration_with_notes_app(self):
        """Integration test with Notes app."""
        # Only runs with: pytest -m integration
        pass
```

### Test Categories

- **Unit Tests**: Fast, isolated tests
- **Integration Tests**: Tests requiring macOS/apps
- **Safety Tests**: Security validation tests

### Running Tests

```bash
# Unit tests only
pytest tests/

# Integration tests
pytest -m integration

# With coverage
pytest --cov=orbit --cov-report=term-missing
```

### Test Coverage

Aim for >80% code coverage. Check coverage report:

```bash
pytest --cov=orbit --cov-report=html
open htmlcov/index.html
```

---

## Documentation

### Code Documentation

All code must include:
- Type hints
- Docstrings for all public functions/classes
- Inline comments for complex logic

### Satellite Documentation

When adding a new satellite:

1. Add to `docs/SATELLITES.md`
2. Add to `docs/SATELLITES_CN.md`
3. Include usage example
4. Document safety level

### Example Documentation

```markdown
## New Satellite

### Satellite

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `new_satellite` | SAFE | Description of what it does |

### Usage Example

```python
mission.launch("new_satellite", {"param": "value"})
```
```

---

## Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows coding standards
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] PR description clearly explains changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. Automated checks run (tests, linting)
2. Maintainer reviews code
3. Feedback provided (if any)
4. Address feedback
5. Approval and merge

---

## Adding Satellites

### Satellite Template

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel

my_satellite = Satellite(
    name="category_action",
    description="Clear description of what this satellite does",
    category="category",
    parameters=[
        SatelliteParameter(
            name="param_name",
            type="string",
            description="Parameter description",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "AppName"
        {{ action_script }}
    end tell
    """,
    result_parser=lambda x: {"result": x},
    examples=[
        {
            "input": {"param": "value"},
            "output": {"result": "expected"}
        }
    ]
)
```

### Best Practices

1. **Safety First**: Choose appropriate safety level
2. **Clear Descriptions**: Help LLMs understand the satellite
3. **Error Handling**: Handle common failures gracefully
4. **Examples**: Provide clear usage examples
5. **Testing**: Add comprehensive tests

---

## Getting Help

### Resources

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **API Reference**: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- **Issues**: https://github.com/xiaoxiath/orbit/issues
- **Discussions**: https://github.com/xiaoxiath/orbit/discussions

### Contact

- **Email**: support@orbit.dev
- **GitHub**: @xiaoxiath

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to join as maintainers (for significant contributions)

Thank you for contributing to Orbit! 🛸

---

**Contributing Guide Version:** 1.0.0
**Last Updated:** 2026-01-27
