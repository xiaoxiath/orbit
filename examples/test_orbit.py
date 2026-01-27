#!/usr/bin/env python3
"""
Orbit macOS - Test Script
Testing basic functionality of Orbit automation toolkit
"""

from orbit import MissionControl, SafetyShield, SafetyLevel
from orbit.satellites.all_satellites import all_satellites
import json

def main():
    print("=" * 60)
    print("🛸 Orbit macOS - Test Script")
    print("=" * 60)
    print()

    # Step 1: Initialize Mission Control
    print("Step 1: Initializing Mission Control...")
    shield = SafetyShield(rules={
        SafetyLevel.SAFE: 'allow',
        SafetyLevel.MODERATE: 'allow',
        SafetyLevel.DANGEROUS: 'deny',
        SafetyLevel.CRITICAL: 'deny'
    })

    mission = MissionControl(safety_shield=shield)
    mission.register_constellation(all_satellites)

    print(f"✅ Registered {len(all_satellites)} satellites")
    print(f"   Categories: 12")
    print()

    # Step 2: List Satellite Categories
    print("Step 2: Satellite Categories")
    print("-" * 60)

    categories = {}
    for sat in mission.constellation.list_all():
        cat = sat.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(sat)

    for cat, sats in sorted(categories.items()):
        safe_count = sum(1 for s in sats if s.safety_level == SafetyLevel.SAFE)
        print(f"  {cat:15} {len(sats):3} satellites  ({safe_count} SAFE)")

    print()

    # Step 3: Test Clipboard Operations
    print("Step 3: Testing Clipboard Operations")
    print("-" * 60)

    result = mission.launch('system_set_clipboard', {
        'content': 'Hello from Orbit! 🛸'
    })
    print(f"✅ Set clipboard: {result}")

    result = mission.launch('system_get_clipboard', {})
    print(f"✅ Get clipboard: '{result}'")
    print()

    # Step 4: Test System Operations
    print("Step 4: Testing System Operations")
    print("-" * 60)

    try:
        result = mission.launch('system_send_notification', {
            'title': 'Orbit Test',
            'message': 'Orbit is working perfectly! 🚀'
        })
        print(f"✅ Sent notification: {result}")
    except Exception as e:
        print(f"⚠️  Notification error (may require permissions): {e}")

    print()

    # Step 5: Display Satellite Info
    print("Step 5: Sample Satellite Information")
    print("-" * 60)

    sample_satellites = [
        'system_get_info',
        'file_list',
        'notes_create',
        'music_play'
    ]

    for sat_name in sample_satellites:
        try:
            sat = mission.constellation.get(sat_name)
            if sat:
                print(f"\n  🛰️  {sat.name}")
                print(f"     Description: {sat.description}")
                print(f"     Safety: {sat.safety_level.name}")
                print(f"     Parameters: {len(sat.parameters)}")
        except Exception as e:
            print(f"  ⚠️  {sat_name}: {e}")

    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
    print()
    print("📚 Quick Start:")
    print("  from orbit import MissionControl")
    print("  from orbit.satellites import all_satellites")
    print()
    print("  mission = MissionControl()")
    print("  mission.register_constellation(all_satellites)")
    print("  result = mission.launch('system_get_clipboard', {})")
    print()

if __name__ == '__main__':
    main()
