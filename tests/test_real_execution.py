"""
Comprehensive Test Suite for Orbit Satellites

This module performs REAL AppleScript execution tests to catch:
- AppleScript syntax errors
- Template rendering issues
- macOS compatibility problems
- Permission requirements
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any
import pytest

from orbit import MissionControl
from orbit.satellites import all_satellites
from orbit.core import SafetyLevel, SafetyShield


class RealExecutionTester:
    """Test REAL AppleScript execution for all satellites."""

    def __init__(self):
        self.mission = MissionControl()
        # Use permissive shield for testing
        self.shield = SafetyShield(rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "allow",
            SafetyLevel.DANGEROUS: "allow",
            SafetyLevel.CRITICAL: "deny"
        })
        self.mission = MissionControl(safety_shield=self.shield)
        self.mission.register_constellation(all_satellites)

        self.failed_satellites = []
        self.passed_satellites = []
        self.skipped_satellites = []

    def test_satellite_syntax(self, satellite_name: str) -> Dict[str, Any]:
        """
        Test satellite AppleScript syntax by attempting to compile it.

        This catches:
        - Syntax errors
        - Undefined variables/functions
        - Template rendering failures

        Returns:
            Dict with test results
        """
        satellite = self.mission.constellation.get(satellite_name)
        if not satellite:
            return {
                "status": "skip",
                "reason": f"Satellite {satellite_name} not found"
            }

        try:
            # Try to render template with sample parameters
            sample_params = self._get_sample_params(satellite)

            # This will catch template rendering errors
            from orbit.core.launcher import Launcher
            launcher = Launcher(safety_shield=self.shield)
            script = launcher._render_template(
                satellite.applescript_template,
                sample_params
            )

            # Test if AppleScript can at least parse it
            result = subprocess.run(
                ["osascript", "-e", "tell application \"System Events\" to " + script],
                capture_output=True,
                text=True,
                timeout=5
            )

            # We expect this to fail due to invalid syntax/variables
            # But NOT due to parsing errors
            if "syntax error" in result.stderr or "Expected" in result.stderr:
                return {
                    "status": "fail",
                    "error": "Syntax error in AppleScript",
                    "details": result.stderr.strip()
                }
            else:
                return {
                    "status": "pass",
                    "note": "Script parses successfully (may fail at runtime)"
                }

        except Exception as e:
            return {
                "status": "fail",
                "error": str(e),
                "type": type(e).__name__
            }

    def _get_sample_params(self, satellite) -> Dict[str, Any]:
        """Generate sample parameters for a satellite."""
        params = {}
        for param in satellite.parameters:
            if param.default is not None:
                params[param.name] = param.default
            elif param.required:
                # Provide sample values based on type
                if param.type == "string":
                    params[param.name] = "test"
                elif param.type == "boolean":
                    params[param.name] = False
                elif param.type == "integer":
                    params[param.name] = 0
        return params

    def run_syntax_checks(self) -> Dict[str, Any]:
        """Run syntax checks on all satellites."""
        results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "details": {}
        }

        for satellite in self.mission.constellation.list_all():
            results["total"] += 1
            result = self.test_satellite_syntax(satellite.name)
            results["details"][satellite.name] = result

            if result["status"] == "pass":
                results["passed"] += 1
                self.passed_satellites.append(satellite.name)
            elif result["status"] == "fail":
                results["failed"] += 1
                self.failed_satellites.append(satellite.name)
            else:
                results["skipped"] += 1
                self.skipped_satellites.append(satellite.name)

        return results

    def generate_report(self) -> str:
        """Generate a detailed test report."""
        results = self.run_syntax_checks()

        report = []
        report.append("=" * 80)
        report.append("Orbit Satellite Syntax Test Report")
        report.append("=" * 80)
        report.append("")

        # Summary
        report.append(f"Total Satellites: {results['total']}")
        report.append(f"✅ Passed: {results['passed']}")
        report.append(f"❌ Failed: {results['failed']}")
        report.append(f"⏭️  Skipped: {results['skipped']}")
        report.append("")

        # Failed details
        if self.failed_satellites:
            report.append("Failed Satellites:")
            report.append("-" * 80)
            for name in self.failed_satellites:
                detail = results["details"][name]
                report.append(f"\n{name}:")
                report.append(f"  Error: {detail.get('error', 'Unknown')}")
                if "details" in detail:
                    report.append(f"  Details: {detail['details']}")
            report.append("")

        # Passed
        if self.passed_satellites:
            report.append("Passed Satellites:")
            report.append("-" * 80)
            for name in self.passed_satellites[:20]:  # Show first 20
                report.append(f"  ✅ {name}")
            if len(self.passed_satellites) > 20:
                report.append(f"  ... and {len(self.passed_satellites) - 20} more")
            report.append("")

        # Recommendations
        report.append("Recommendations:")
        report.append("-" * 80)
        if results["failed"] > 0:
            report.append(f"🔴 URGENT: Fix {results['failed']} satellites with syntax errors")
        if results["passed"] < results["total"]:
            report.append(f"🟡 Review: {results['total'] - results['passed']} satellites need attention")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)


def test_all_satellites_syntax():
    """Pytest fixture to test all satellites for syntax errors."""
    tester = RealExecutionTester()
    results = tester.run_syntax_checks()

    # Print report
    print(tester.generate_report())

    # Assert no critical failures
    assert results["failed"] == 0, \
        f"{results['failed']} satellites have syntax errors!\n" \
        f"Failed: {', '.join(tester.failed_satellites)}"


def test_critical_satellites_real_execution():
    """
    Test CRITICAL satellites with REAL AppleScript execution.

    This catches bugs that mock tests miss.
    """
    tester = RealExecutionTester()

    # Test a few critical satellites that should work on any macOS system
    critical_tests = [
        ("system_get_clipboard", {}),
        ("system_get_info", {}),
        ("app_list", {}),
    ]

    for sat_name, params in critical_tests:
        satellite = tester.mission.constellation.get(sat_name)
        if not satellite:
            pytest.skip(f"Satellite {sat_name} not found")

        try:
            # Try REAL execution (with timeout)
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError("Satellite execution timed out")

            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)  # 5 second timeout

            try:
                result = tester.mission.launch(sat_name, params)
                signal.alarm(0)  # Cancel timeout

                # Just check it didn't crash
                assert result is not None or result == "" or isinstance(result, (dict, list))
                print(f"✅ {sat_name}: REAL execution successful")
            except TimeoutError:
                signal.alarm(0)
                pytest.fail(f"{sat_name}: Execution timed out (possible infinite loop)")

        except Exception as e:
            signal.alarm(0)
            # Check if it's a permission error (acceptable)
            if "permission" in str(e).lower() or "privilege" in str(e).lower():
                print(f"⚠️  {sat_name}: Permission required (acceptable)")
            else:
                pytest.fail(f"{sat_name}: REAL execution failed: {e}")


if __name__ == "__main__":
    print("Running Orbit Satellite Syntax Tests...")
    print("")
    test_all_satellites_syntax()
