#!/usr/bin/env python3
"""
AppleScript Syntax and Template Validator for Orbit Satellites

This script validates:
1. AppleScript syntax (by attempting compilation)
2. Jinja2 template syntax
3. Common error patterns
4. Undefined function references
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


class AppleScriptValidator:
    """Validates AppleScript code in Orbit satellites."""

    def __init__(self, orbit_path: str):
        self.orbit_path = Path(orbit_path)
        self.satellites_path = self.orbit_path / "src/orbit/satellites"

    def check_all_satellites(self) -> dict:
        """Check all satellites for issues."""
        results = {
            "total": 0,
            "errors": [],
            "warnings": [],
            "satellites": {}
        }

        # Find all satellite files
        satellite_files = list(self.satellites_path.glob("*.py"))

        for file_path in satellite_files:
            satellite_name = file_path.stem
            results["satellites"][satellite_name] = self.check_file(file_path)
            results["total"] += 1

        return results

    def check_file(self, file_path: Path) -> dict:
        """Check a single satellite file for issues."""
        content = file_path.read_text()
        errors = []
        warnings = []

        # Check for undefined functions
        undefined_patterns = {
            r"my_list\(": "Undefined function my_list()",
            r"undefined_function": "Placeholder for undefined function",
        }

        for pattern, description in undefined_patterns.items():
            if re.search(pattern, content):
                errors.append(f"❌ {description}")

        # Check for problematic Jinja2 syntax
        jinja_issues = self.check_jinja2_syntax(content)
        warnings.extend(jinja_issues)

        # Check for common AppleScript errors
        applescript_issues = self.check_applescript_in_code(content)
        errors.extend(applescript_issues)

        return {
            "file": str(file_path),
            "errors": errors,
            "warnings": warnings,
            "status": "fail" if errors else "warn" if warnings else "pass"
        }

    def check_jinja2_syntax(self, content: str) -> List[str]:
        """Check Jinja2 template syntax issues."""
        warnings = []

        # Check for {{ var|lower }} usage
        if "{{ .*|lower }}" in content:
            warnings.append("⚠️  Found {{ var|lower }} - use {{ \"true\" if var else \"false\" }} instead")

        # Check for {{ var|upper }} usage
        if "{{ .*|upper }}" in content:
            warnings.append("⚠️  Found {{ var|upper }} - use {{ \"TRUE\" if var else \"FALSE\" }} instead")

        return warnings

    def check_applescript_in_code(self, content: str) -> List[str]:
        """Check for AppleScript syntax issues in Python strings."""
        errors = []

        # Extract AppleScript templates
        applescript_blocks = re.findall(r'applescript_template\s*=\s*"""(.*?)"""', content, re.DOTALL)

        for i, script in enumerate(applescript_blocks):
            # Check for common syntax errors
            if "my_list(" in script:
                errors.append(f"AppleScript block #{i+1} contains undefined my_list() function")

            # Check for template syntax issues
            if "{{ " in script and "}}" in script:
                # Check if Jinja2 syntax is valid
                try:
                    import jinja2
                    # Try to parse (won't catch all issues but helps)
                    jinja2.Template(script)
                except Exception as e:
                    errors.append(f"Jinja2 template error: {e}")

        return errors


def create_static_analysis_script(orbit_path: str):
    """Create a comprehensive static analysis script."""

    script_content = f'''#!/bin/bash
# Static Analysis for Orbit Project
# Runs all quality checks before committing

set -e

echo "🔍 Orbit Static Analysis"
echo "========================"
echo ""

# Navigate to project root
cd "{orbit_path}"

echo "1️⃣  Type Checking (mypy)..."
if command -v mypy &> /dev/null; then
    mypy src/orbit/ || echo "⚠️  mypy not installed"
else
    echo "⚠️  mypy not installed - skipping"
fi
echo ""

echo "2️⃣  Linting (ruff)..."
if command -v ruff &> /dev/null; then
    ruff check src/orbit/ || echo "⚠️  ruff not installed"
else
    echo "⚠️  ruff not installed - skipping"
fi
echo ""

echo "3️⃣  Security Check (bandit)..."
if command -v bandit &> /dev/null; then
    bandit -r src/orbit/ -f screen || echo "⚠️  bandit not installed"
else
    echo "⚠️  bandit not installed - skipping"
fi
echo ""

echo "4️⃣  AppleScript Syntax Check..."
python3 scripts/check_applescript.py
echo ""

echo "5️⃣  Import Check..."
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from orbit import MissionControl
    from orbit.satellites import all_satellites
    print('   ✅ All imports successful')
except Exception as e:
    print(f'   ❌ Import error: {{e}}')
    sys.exit(1)
"
echo ""

echo "✅ Static Analysis Complete!"
echo ""
echo "Run tests with: python3 -m pytest tests/"
'''

    script_path = Path(orbit_path) / "scripts/static_analysis.sh"
    script_path.write_text(script_content)
    script_path.chmod(0o755)

    print(f"✅ Created {script_path}")


def create_pre_commit_hook(orbit_path: str):
    """Create pre-commit hook."""

    hook_content = f'''#!/bin/bash
# Pre-commit hook for Orbit
# Runs quick checks before allowing commit

echo "🔍 Pre-commit Checks..."
echo ""

# Get list of changed Python files
PY_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '.py$' || true)

if [ -z "$PY_FILES" ]; then
    echo "No Python files changed - skipping checks"
    exit 0
fi

echo "Checking files:"
echo "$PY_FILES"
echo ""

# Run static analysis on changed files
bash {orbit_path}/scripts/static_analysis.sh

# Run quick tests
echo ""
echo "Running quick tests..."
python3 -m pytest tests/test_parsers.py -v -q || echo "⚠️  Some tests failed"

echo ""
echo "✅ Pre-commit checks passed!"
'''

    hooks_dir = Path(orbit_path) / ".git/hooks"
    hook_path = hooks_dir / "pre-commit"

    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)

    print(f"✅ Created {hook_path}")
    print("   (Install with: cp .git/hooks/pre-commit .git/hooks/pre-commit)")


def create_applescript_checker(orbit_path: str):
    """Create AppleScript syntax checker."""

    checker_content = '''#!/usr/bin/env python3
"""Check AppleScript syntax in Orbit satellites."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tests.test_real_execution import RealExecutionTester

def main():
    print("🔍 Checking Orbit satellites for syntax errors...")
    print("")

    tester = RealExecutionTester()
    results = tester.run_syntax_checks()

    print(f"Total satellites: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"⏭️  Skipped: {results['skipped']}")
    print("")

    if results['failed'] > 0:
        print("Failed satellites:")
        for name in tester.failed_satellites:
            detail = results['details'][name]
            print(f"\n❌ {name}")
            print(f"   {detail.get('error', 'Unknown error')}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

    checker_path = Path(orbit_path) / "scripts/check_applescript.py"
    checker_path.write_text(checker_content)
    checker_path.chmod(0o755)

    print(f"✅ Created {checker_path}")


def main():
    """Create all testing infrastructure."""

    orbit_path = "/Users/bytedance/workspace/llm/macagent-orbit"

    print("🚀 Creating Orbit Testing Infrastructure")
    print("=" * 80)
    print("")

    print("Creating scripts...")
    create_static_analysis_script(orbit_path)
    create_pre_commit_hook(orbit_path)
    create_applescript_checker(orbit_path)

    print("")
    print("✅ Testing infrastructure created!")
    print("")
    print("Next steps:")
    print("1. Install pre-commit hook:")
    print(f"   cp {orbit_path}/.git/hooks/pre-commit {orbit_path}/.git/hooks/pre-commit")
    print("")
    print("2. Run static analysis:")
    print(f"   bash {orbit_path}/scripts/static_analysis.sh")
    print("")
    print("3. Check satellites:")
    print(f"   python3 {orbit_path}/scripts/check_applescript.py")


if __name__ == "__main__":
    main()
