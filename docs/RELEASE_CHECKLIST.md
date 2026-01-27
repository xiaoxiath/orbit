# Orbit Release Checklist

## Pre-Release

### Code Quality
- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Code coverage > 80% (`pytest --cov=orbit`)
- [ ] No linting errors (`flake8 src/orbit`)
- [ ] Type checking passing (`mypy src/orbit`)
- [ ] Documentation examples tested

### Documentation
- [ ] README.md up to date
- [ ] README_CN.md up to date
- [ ] API_REFERENCE.md complete
- [ ] API_REFERENCE_CN.md complete
- [ ] DESIGN.md accurate
- [ ] DESIGN_CN.md accurate
- [ ] SECURITY.md updated
- [ ] SECURITY_CN.md updated
- [ ] QUICKSTART.md tested
- [ ] QUICKSTART_CN.md tested
- [ ] All examples run successfully
  - [ ] examples/basic_usage.py
  - [ ] examples/openai_functions.py
  - [ ] examples/openai_integration.py
  - [ ] examples/langchain_integration.py
  - [ ] examples/anthropic_integration.py
  - [ ] examples/custom_agent.py
  - [ ] examples/comprehensive_demo.py

### Version
- [ ] Version number updated in `pyproject.toml`
- [ ] CHANGELOG.md updated with release notes
- [ ] Git tag created (e.g., `v1.0.0`)

### Dependencies
- [ ] All dependencies listed in pyproject.toml
- [ ] No unnecessary dependencies
- [ ] License compatible with all dependencies

### Security
- [ ] No hardcoded secrets or API keys
- [ ] Safety shield properly configured
- [ ] Protected paths validated
- [ ] Dangerous commands filtered

## Release Process

### Step 1: Final Testing
```bash
# Run full test suite
poetry install --with dev
poetry run pytest tests/ -v

# Test examples
poetry run python examples/basic_usage.py
poetry run python examples/comprehensive_demo.py

# Build package
poetry build
```

### Step 2: Create Git Tag
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Step 3: Publish to PyPI
```bash
# Test on TestPyPI first
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

# Then publish to PyPI
poetry publish
```

### Step 4: GitHub Release
- [ ] Create release on GitHub
- [ ] Upload built artifacts (wheel and tar.gz)
- [ ] Copy release notes from CHANGELOG.md
- [ ] Link to documentation

### Step 5: Announcements
- [ ] Update project website
- [ ] Post on social media
- [ ] Notify community
- [ ] Send to mailing list

## Post-Release

### Monitoring
- [ ] Watch PyPI downloads
- [ ] Monitor GitHub issues
- [ ] Check for bug reports
- [ ] Track usage metrics

### Maintenance
- [ ] Respond to issues within 24 hours
- [ ] Review and merge PRs
- [ ] Update documentation as needed
- [ ] Plan next release

## Version Bumping

For semantic versioning (MAJOR.MINOR.PATCH):

### MAJOR (X.0.0)
- Breaking changes
- API changes
- Removed features

### MINOR (0.X.0)
- New features
- Enhancements
- Backward-compatible changes

### PATCH (0.0.X)
- Bug fixes
- Security patches
- Documentation updates
- Small improvements

## Emergency Release Process

If critical bug found:

1. Create hotfix branch from main
2. Fix the issue
3. Update PATCH version
4. Run full test suite
5. Create release tag
6. Publish to PyPI
7. Merge hotfix back to main
8. Announce fix

## Rollback Plan

If release has critical issues:

1. Yank package from PyPI (`pip yank`)
2. Create GitHub issue documenting problem
3. Fix in hotfix branch
4. Release new version with fix
5. Announce issue and fix

## Release History Template

```markdown
# [Version] - [Date]

## Added
- New feature 1
- New feature 2

## Changed
- Updated feature 1
- Improved feature 2

## Fixed
- Bug fix 1
- Bug fix 2

## Removed
- Deprecated feature 1

## Security
- Security fix 1
```

## Checklist Files

- [x] RELEASE_CHECKLIST.md (this file)
- [ ] CHANGELOG.md (needs to be created)
- [ ] .github/workflows/ci.yml (created)
- [ ] pyproject.toml (verify version)

## Notes

- Always test on macOS before releasing (requires macOS-specific features)
- Keep CI/CD pipeline green before releases
- Document all breaking changes
- Provide migration guide for major versions
- Maintain backward compatibility when possible
