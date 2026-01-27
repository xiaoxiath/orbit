#!/usr/bin/env python3
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
