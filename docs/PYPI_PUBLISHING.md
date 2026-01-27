# PyPI Package Publishing Guide

> **Orbit macOS Automation Toolkit**
> Version: 1.0.0

This guide explains how to publish the `orbit-macos` package to PyPI (Python Package Index).

---

## Prerequisites

### 1. Install Poetry

Poetry is used for dependency management and packaging.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify installation:
```bash
poetry --version
```

### 2. Install Twine

Twine is used for securely uploading packages to PyPI.

```bash
pip install twine
```

### 3. PyPI Account

You need a PyPI account:
- **Production**: https://pypi.org/account/register/
- **Test**: https://test.pypi.org/account/register/

**Important**: Enable 2-Factor Authentication and create an API token for authentication.

---

## Publishing Workflow

### Step 1: Update Version (if needed)

Edit `pyproject.toml`:

```toml
[tool.poetry]
name = "orbit-macos"
version = "1.0.0"  # Update this
```

### Step 2: Build the Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build with Poetry
poetry build
```

This creates:
- `dist/orbit-macos-1.0.0.tar.gz` - Source distribution
- `dist/orbit_macos-1.0.0-py3-none-any.whl` - Wheel distribution

### Step 3: Check the Package

Verify the package metadata:
```bash
twine check dist/*
```

Expected output:
```
Checking orbit-macos-1.0.0.tar.gz: PASSED
Checking orbit_macos-1.0.0-py3-none-any.whl: PASSED
```

### Step 4: Test Publish (Recommended)

First publish to TestPyPI to verify everything works:

```bash
# Configure TestPyPI credentials in ~/.pypirc
twine upload --repository testpypi dist/*
```

Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ orbit-macos
```

### Step 5: Publish to PyPI

Once testing is successful, publish to production PyPI:

```bash
twine upload dist/*
```

---

## Authentication

### Option 1: API Token (Recommended)

1. Go to https://pypi.org/manage/account/token/
2. Create a new token with "Entire account" scope
3. Use token as password with username `__token__`

```bash
twine upload dist/* --username __token__ --password <your-token>
```

### Option 2: ~/.pypirc Configuration

Create `~/./.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = <your-pypi-token>

[testpypi]
username = __token__
password = <your-testpypi-token>
repository = https://test.pypi.org/legacy/
```

Then upload without prompts:
```bash
twine upload dist/*  # PyPI
twine upload --repository testpypi dist/*  # TestPyPI
```

---

## Automated Script

Use the provided script for automated publishing:

```bash
./scripts/publish_to_pypi.sh
```

This script:
- ✅ Checks prerequisites (Poetry, Twine)
- ✅ Displays current version
- ✅ Cleans old build files
- ✅ Builds package with Poetry
- ✅ Checks package with Twine
- ✅ Prompts for destination (TestPyPI/PyPI)
- ✅ Uploads to chosen repository
- ✅ Displays installation instructions

---

## Verification

After publishing, verify the package:

### Check PyPI Page
- **Production**: https://pypi.org/project/orbit-macos/
- **Test**: https://test.pypi.org/project/orbit-macos/

### Test Installation

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install orbit-macos

# Test import
python -c "from orbit import MissionControl; print('✅ Import successful')"

# Test CLI
orbit --version

# Cleanup
deactivate
rm -rf test_env
```

### Run Basic Tests

```bash
# After installation
python -c "
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# Test basic satellite
result = mission.launch('system_get_info', {})
print(f'MacOS Version: {result.get(\"version\", \"unknown\")}')
print('✅ All tests passed!')
"
```

---

## Common Issues

### Issue: "Package already exists"

This error occurs when trying to upload a version that's already published.

**Solution**: Increment version in `pyproject.toml` and rebuild.

### Issue: "403 Forbidden"

Authentication failed.

**Solution**:
1. Verify API token is valid
2. Check `~/.pypirc` configuration
3. Use `__token__` as username

### Issue: "Invalid or missing authentication credentials"

Twine can't find credentials.

**Solution**: Create `~/.pypirc` with your token (see Authentication section).

### Issue: Build fails

Poetry build fails due to errors.

**Solution**:
```bash
# Check poetry.lock is up to date
poetry lock --no-update

# Validate pyproject.toml
poetry check

# Try building again
poetry build
```

---

## Version Bumping Checklist

When releasing a new version:

- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG.md with release notes
- [ ] Update version references in documentation
- [ ] Run full test suite: `poetry run pytest`
- [ ] Build package: `poetry build`
- [ ] Test locally: `pip install dist/orbit_macos-*.whl`
- [ ] Upload to TestPyPI first
- [ ] Install from TestPyPI and verify
- [ ] Upload to production PyPI
- [ ] Verify on https://pypi.org/project/orbit-macos/
- [ ] Create GitHub release with tag
- [ ] Announce release

---

## Project Configuration

Current `pyproject.toml` settings:

```toml
[tool.poetry]
name = "orbit-macos"
version = "1.0.0"
description = "🛸 Orbit: Your AI's Bridge to macOS - Framework-agnostic automation toolkit with 104+ satellites"

[tool.poetry.dependencies]
python = "^3.10"
jinja2 = "^3.1.0"
structlog = "^23.0.0"
pydantic = "^2.0.0"
click = "^8.1.0"
```

**Key Points**:
- Package name: `orbit-macos` (install with `pip install orbit-macos`)
- Import name: `orbit` (use `from orbit import MissionControl`)
- Python: 3.10+
- CLI command: `orbit`

---

## Post-Release Tasks

After successful release:

1. **Tag the release in Git**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Create GitHub Release**:
   - Go to: https://github.com/xiaoxiath/orbit/releases/new
   - Tag: `v1.0.0`
   - Title: `🛸 Orbit v1.0.0 - Your AI's Bridge to macOS`
   - Description: Copy from CHANGELOG.md

3. **Update Documentation**:
   - Update installation instructions to point to PyPI
   - Add badge to README: `[![PyPI version](https://badge.fury.io/py/orbit-macos.svg)](https://pypi.org/project/orbit-macos/)`

4. **Announce**:
   - Twitter/X
   - Project discussions
   - Community channels

---

## Quick Reference

```bash
# Full release workflow
rm -rf dist/ build/ *.egg-info
poetry build
twine check dist/*
twine upload --repository testpypi dist/*  # Test first
pip install --index-url https://test.pypi.org/simple/ orbit-macos  # Verify
twine upload dist/*  # Production
```

---

**Last Updated**: 2026-01-27
**Current Version**: 1.0.0
**Package URL**: https://pypi.org/project/orbit-macos/
