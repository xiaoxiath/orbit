#!/usr/bin/env python3
"""Quick AppleScript syntax checker for Orbit."""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def check_satellites():
    """Quick check for common satellite issues."""
    print("🔍 Quick Orbit Satellite Check")
    print("=" * 60)
    print("")

    issues_found = []

    # Check 1: my_list usage
    print("Checking for common issues...")
    print("")

    import subprocess
    result = subprocess.run(
        ["grep", "-r", "my_list", "src/orbit/satellites/"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    if "my_list" in result.stdout:
        print("❌ Found: my_list() function (undefined)")
        print("   Fix: Replace with proper AppleScript")
        issues_found.append("my_list")

    # Check 2: Jinja2 filter syntax
    result = subprocess.run(
        ["grep", "-r", "{{ .*|lower }}", "src/orbit/satellites/"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    if "{{" in result.stdout and "|lower}}" in result.stdout:
        print("⚠️  Found: {{ var|lower }} filter")
        print("   Suggestion: Use {{ \"true\" if var else \"false\" }}")
        issues_found.append("jinja2_filters")

    # Summary
    print("")
    print("=" * 60)
    if issues_found:
        print(f"❌ Found {len(issues_found)} issue(s)")
        return 1
    else:
        print("✅ No obvious issues found!")
        return 0

if __name__ == "__main__":
    sys.exit(check_satellites())
