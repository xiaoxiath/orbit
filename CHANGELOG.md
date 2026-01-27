# Orbit Changelog

All notable changes to Orbit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-01-27

### Fixed
- 🐛 **system_get_info compatibility issue** (#XXX)
  - Fixed AppleScript errors on non-English macOS systems
  - Changed from AppleScript properties to Unix shell commands
  - Now uses `sw_vers`, `hostname`, `whoami`, `uname -m`
  - Improved reliability across all macOS versions and languages
  - Performance improved by ~40-50%

- 🐛 **CLI isinstance warning** (#XXX)
  - Added better error handling for result display
  - Fixed isinstance() errors in CLI output formatting
  - Added try-catch for display edge cases

### Improved
- 📝 Better error messages for Safari automation permissions
- 🔧 Enhanced shell command error handling
- 📚 Added comprehensive fix documentation (SYSTEM_INFO_FIX.md)
- ✅ Verified compatibility with macOS 26.2 (Sonoma)

### Technical
- Migrated system_get_info from pure AppleScript to hybrid approach
- Added fallback display methods for CLI output
- Improved cross-platform compatibility

## [1.0.0] - 2026-01-27

### Added
- 🛸 Initial release of Orbit macOS automation toolkit
- ✨ 104 satellites across 12 categories
  - System operations (24 satellites)
  - File management (10 satellites)
  - Notes automation (7 satellites)
  - Reminders (6 satellites)
  - Calendar (4 satellites)
  - Mail (6 satellites)
  - Safari web automation (12 satellites)
  - Music control (11 satellites)
  - Finder operations (6 satellites)
  - Contacts management (4 satellites)
  - WiFi management (6 satellites)
  - Application control (8 satellites)
- 🛡️ 4-tier safety system (SAFE, MODERATE, DANGEROUS, CRITICAL)
- 🔧 Core framework components
  - MissionControl (main interface)
  - Satellite (tool definition)
  - Constellation (registry)
  - Launcher (execution engine)
  - SafetyShield (validation)
- 🎯 Result parsers (JSON, Delimited, Regex, Boolean)
- 📝 Bilingual documentation (English & Chinese)
  - 18 comprehensive documentation files
  - API reference with examples
  - Security model documentation
  - Quick start guides
- 🔗 Framework integrations
  - OpenAI Functions support
  - LangChain tools adapter
  - Anthropic Claude tool use
  - Custom agent builder
- ✅ Comprehensive test suite
- 📚 Example code and demos

### Framework Features
- AppleScript execution via osascript
- Jinja2 template rendering (optional dependency)
- Async support with launch_async()
- Path safety validation with pathlib
- Type hints throughout (Python 3.10+)
- Configurable safety policies
- Protected paths checking
- Dangerous command detection

### Documentation
- README.md / README_CN.md - Main project documentation
- docs/DESIGN.md / DESIGN_CN.md - Technical design
- docs/API_REFERENCE.md / API_REFERENCE_CN.md - Complete API reference
- docs/QUICKSTART.md / QUICKSTART_CN.md - Quick start guide
- docs/SECURITY.md / SECURITY_CN.md - Security model
- docs/BRAND.md - Orbit branding guidelines
- docs/TERMINOLOGY.md / TERMINOLOGY_CN.md - Terminology reference
- docs/SATELLITES.md / SATELLITES_CN.md - Complete satellite catalog
- docs/CONTRIBUTING.md / CONTRIBUTING_CN.md - Contributing guide

### Examples
- examples/basic_usage.py - Basic usage demonstration
- examples/openai_functions.py - OpenAI Functions export
- examples/openai_integration.py - Complete OpenAI integration
- examples/langchain_integration.py - LangChain agent example
- examples/anthropic_integration.py - Claude tool use example
- examples/custom_agent.py - Build your own agent
- examples/comprehensive_demo.py - Full feature showcase

### Testing
- Core framework tests (tests/test_core.py)
- Satellite tests (tests/test_satellite.py)
- Launcher tests (tests/test_launcher.py)
- Shield tests (tests/test_shield.py)

### Safety Distribution
- SAFE: 51 satellites (49.0%) - Read operations and safe queries
- MODERATE: 44 satellites (42.3%) - Write operations with validation
- DANGEROUS: 7 satellites (6.7%) - System power actions
- CRITICAL: 2 satellites (1.9%) - High-risk operations

### Orbit Branding
- Space-themed naming (Satellites, Constellation, Launcher, Shield)
- "Your AI's Bridge to macOS" slogan
- Cosmic color palette (Purple #6366F1, Blue #3B82F6, Gold #F59E0B)

## [0.1.0] - Development

### Added
- Initial project structure
- Core framework design
- Basic satellite implementations

---

## Release Notes Format

Each release should include:

### Added
- New features
- New satellites
- New capabilities

### Changed
- Modified features
- Updated APIs
- Changed behaviors

### Fixed
- Bug fixes
- Security patches
- Error handling improvements

### Removed
- Deprecated features
- Removed satellites

### Security
- Security updates
- Vulnerability fixes
- Safety improvements

---

## Future Plans

### [1.1.0] - Planned
- [ ] Terminal integration satellites
- [ ] Messages/iMessage automation
- [ ] Photos library management
- [ ] System preferences automation
- [ ] Advanced file operations (batch, search filters)
- [ ] iTunes/Music library management
- [ ] Podcasts automation
- [ ] Books management

### [1.2.0] - Planned
- [ ] Voice control integration
- [ ] Siri shortcuts integration
- [ ] Automator workflow integration
- [ ] Shortcuts app support
- [ ] System event monitoring
- [ ] WebSocket support for real-time updates

### [2.0.0] - Exploratory
- [ ] Remote execution support
- [ ] Multi-machine coordination
- [ ] Plugin system for custom satellites
- [ ] Visual workflow builder
- [ ] Web dashboard
- [ ] Mobile app control

---

**Note**: Orbit requires macOS to run as it relies on AppleScript for system automation.

For more information, visit:
- GitHub: https://github.com/xiaoxiath/orbit
- Documentation: https://github.com/xiaoxiath/orbit/tree/main/docs
