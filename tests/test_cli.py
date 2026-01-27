#!/usr/bin/env python3
"""
Test script for Orbit CLI functionality.

Run this to verify the CLI tool is working correctly.
"""

import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_cli_import():
    """Test CLI module can be imported."""
    try:
        from orbit.cli import cli
        print("✅ CLI module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import CLI: {e}")
        return False


def test_cli_commands():
    """Test CLI commands are registered."""
    try:
        from orbit.cli import cli
        commands = list(cli.commands.keys())

        expected_commands = [
            'list',
            'search',
            'run',
            'interactive',
            'export',
            'version',
            'test'
        ]

        print("\n📋 Registered commands:")
        for cmd in expected_commands:
            if cmd in commands:
                print(f"  ✅ {cmd}")
            else:
                print(f"  ❌ {cmd} (missing)")

        missing = set(expected_commands) - set(commands)
        if not missing:
            print(f"\n✅ All {len(expected_commands)} commands registered")
            return True
        else:
            print(f"\n❌ Missing commands: {missing}")
            return False

    except Exception as e:
        print(f"❌ Error checking commands: {e}")
        return False


def test_colors():
    """Test color output."""
    try:
        from orbit.cli import Colors

        print("\n🎨 Testing colors:")
        print(f"  {Colors.HEADER}HEADER{Colors.ENDC}")
        print(f"  {Colors.OKBLUE}OKBLUE{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}OKGREEN{Colors.ENDC}")
        print(f"  {Colors.WARNING}WARNING{Colors.ENDC}")
        print(f"  {Colors.FAIL}FAIL{Colors.ENDC}")
        print("  ✅ Colors working")
        return True
    except Exception as e:
        print(f"❌ Color test failed: {e}")
        return False


def test_mission_control():
    """Test MissionControl initialization."""
    try:
        from orbit import MissionControl
        from orbit.satellites.all_satellites import all_satellites

        mission = MissionControl()
        for satellite in all_satellites:
            mission.register(satellite)

        print(f"\n✅ MissionControl initialized with {len(all_satellites)} satellites")
        return True
    except Exception as e:
        print(f"\n❌ MissionControl failed: {e}")
        return False


def test_satellite_formatting():
    """Test satellite formatting."""
    try:
        from orbit.cli import format_satellite_info
        from orbit import Satellite, SafetyLevel

        satellite = Satellite(
            name="test_sat",
            description="Test satellite for CLI",
            category="test",
            parameters=[],
            safety_level=SafetyLevel.SAFE,
            applescript_template='return "test"',
        )

        info = format_satellite_info(satellite)
        print(f"\n📄 Formatted satellite info:")
        print(info)

        if "test_sat" in info and "SAFE" in info:
            print("  ✅ Formatting working")
            return True
        else:
            print("  ❌ Formatting incomplete")
            return False

    except Exception as e:
        print(f"\n❌ Formatting test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("🧪 Orbit CLI Test Suite")
    print("=" * 70)

    tests = [
        ("Import CLI module", test_cli_import),
        ("Check CLI commands", test_cli_commands),
        ("Test color output", test_colors),
        ("Initialize MissionControl", test_mission_control),
        ("Test satellite formatting", test_satellite_formatting),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{'=' * 70}")
        print(f"Testing: {name}")
        print('=' * 70)
        result = test_func()
        results.append((name, result))

    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        color = "\033[92m" if result else "\033[91m"
        print(f"{color}{status}\033[0m {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n✨ All tests passed! Orbit CLI is ready to use.\n")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
