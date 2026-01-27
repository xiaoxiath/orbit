"""Comprehensive example demonstrating all Orbit features."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from orbit import MissionControl, SafetyShield, SafetyLevel
from orbit.satellites.all_satellites import all_satellites
from orbit.satellites import (
    system,
    files,
    notes,
    reminders,
    calendar,
)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def demo_system_satellites():
    """Demonstrate system satellites."""
    print_section("🛰️  System Telemetry Satellites")

    mission = MissionControl()
    mission.register(system.system_get_info)

    # Get system info
    print("📊 System Information:")
    try:
        info = mission.launch("system_get_info", {})
        for key, value in info.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"   Note: Run on macOS to execute: {e}")

    # Send notification
    print("\n📢 Sending Notification:")
    print("   Launching system_send_notification...")


def demo_file_satellites():
    """Demonstrate file satellites."""
    print_section("📁 File Communication Satellites")

    mission = MissionControl()

    # Register file satellites
    file_satellites = [
        files.file_list,
        files.file_create_directory,
        files.file_get_info,
    ]
    mission.register_constellation(file_satellites)

    # Show available satellites
    print("🛰️  Registered File Satellites:")
    for sat in mission.constellation.list_all():
        print(f"   - {sat.name}: {sat.description}")

    # Example: Get file info
    print("\n📄 Get File Info Example:")
    print("   mission.launch('file_get_info', {'path': '~/Documents'})")


def demo_app_satellites():
    """Demonstrate app station satellites."""
    print_section("📱 Application Station Satellites")

    mission = MissionControl()

    # Notes
    print("📝 Notes Station:")
    notes_count = len([sat for sat in notes.__all__ if sat.startswith("notes_")])
    print(f"   - Registered: {notes_count} satellites")
    print("   - Examples: notes_create, notes_list, notes_search")

    # Reminders
    print("\n⏰ Reminders Station:")
    reminders_count = len([sat for sat in reminders.__all__ if sat.startswith("reminders_")])
    print(f"   - Registered: {reminders_count} satellites")
    print("   - Examples: reminders_create, reminders_list, reminders_complete")

    # Calendar
    print("\n📅 Calendar Station:")
    calendar_count = len([sat for sat in calendar.__all__ if sat.startswith("calendar_")])
    print(f"   - Registered: {calendar_count} satellites")
    print("   - Examples: calendar_create_event, calendar_get_events")


def demo_safety_levels():
    """Demonstrate safety levels."""
    print_section("🛡️  Safety Shield System")

    mission = MissionControl()
    mission.register_constellation(all_satellites)

    # Get statistics by safety level
    stats = mission.constellation.get_stats()

    print("📊 Satellites by Safety Level:")
    for level, count in stats['by_safety'].items():
        percentage = (count / stats['total_satellites'] * 100) if stats['total_satellites'] > 0 else 0
        level_emoji = {
            'safe': '✅',
            'moderate': '⚠️ ',
            'dangerous': '⚡',
            'critical': '🔴'
        }.get(level, '•')

        print(f"   {level_emoji} {level.upper():12} {count:3} satellites ({percentage:.1f}%)")


def demo_openai_functions():
    """Demonstrate OpenAI Functions export."""
    print_section("🤖 OpenAI Functions Integration")

    mission = MissionControl()
    mission.register(system.system_get_info)
    mission.register(system.system_send_notification)

    # Export to OpenAI Functions format
    functions = mission.export_openai_functions()

    print("📋 Exported Functions:")
    for func in functions:
        print(f"   - {func['function']['name']}")
        print(f"     Description: {func['function']['description']}")

        if func['function']['parameters']['properties']:
            print(f"     Parameters:")
            for param_name, param_info in func['function']['parameters']['properties'].items():
                required = param_name in func['function']['parameters']['required']
                req_str = "required" if required else "optional"
                print(f"       • {param_name} ({param_info['type']}, {req_str})")


def demo_custom_safety():
    """Demonstrate custom safety configuration."""
    print_section("🔧 Custom Safety Configuration")

    print("Option 1: Strict Mode (SAFE only)")
    strict_shield = SafetyShield(
        rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "deny",
            SafetyLevel.DANGEROUS: "deny",
            SafetyLevel.CRITICAL: "deny"
        }
    )
    mission_strict = MissionControl(safety_shield=strict_shield)
    mission_strict.register(system.system_get_info)  # SAFE
    print(f"   ✓ SAFE operations allowed")
    print(f"   ✗ MODERATE+ operations blocked")

    print("\nOption 2: Permissive Mode (allow all)")
    permissive_shield = SafetyShield(
        rules={level: "allow" for level in SafetyLevel}
    )
    print(f"   ✓ All operations allowed")

    print("\nOption 3: Confirmation Mode (require confirmation)")
    def confirm_callback(satellite, parameters):
        print(f"   ⚠️  Confirmation required for {satellite.name}")
        # For demo, auto-confirm
        return True

    confirm_shield = SafetyShield(
        rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "confirm",
            SafetyLevel.DANGEROUS: "confirm",
        },
        confirmation_callback=confirm_callback
    )
    print(f"   ✓ SAFE operations auto-allowed")
    print(f"   ⚠️  MODERATE/DANGEROUS require confirmation")


def demo_statistics():
    """Show constellation statistics."""
    print_section("📊 Constellation Statistics")

    mission = MissionControl()
    mission.register_constellation(all_satellites)

    stats = mission.constellation.get_stats()

    print(f"Total Satellites: {stats['total_satellites']}")
    print(f"Categories: {stats['categories']}")

    print("\nBy Category:")
    categories = mission.constellation.get_categories()
    for category in sorted(categories):
        count = len(mission.constellation.list_by_category(category))
        print(f"   {category:20} {count:3} satellites")

    print("\nBy Safety Level:")
    for level, count in stats['by_safety'].items():
        percentage = (count / stats['total_satellites'] * 100)
        print(f"   {level.upper():12} {count:3} ({percentage:.1f}%)")


def main():
    """Run comprehensive demo."""
    print("""
🛸  Orbit - Comprehensive Feature Demo
==========================================

This demo showcases all Orbit capabilities including:
  • System Telemetry Satellites
  • File Communication Satellites
  • Application Station Satellites (Notes, Reminders, Calendar)
  • Safety Shield System
  • OpenAI Functions Integration
  • Custom Safety Configuration
  • Constellation Statistics
    """)

    try:
        demo_system_satellites()
        demo_file_satellites()
        demo_app_satellites()
        demo_safety_levels()
        demo_openai_functions()
        demo_custom_safety()
        demo_statistics()

        print("\n" + "=" * 70)
        print("✅ Demo Complete!")
        print("\n🚀 Next Steps:")
        print("   1. Run on macOS to execute AppleScript commands")
        print("   2. Check examples/ directory for more examples")
        print("   3. Read docs/ for complete documentation")
        print("\n🛸 Orbit - Your AI's bridge to macOS")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
