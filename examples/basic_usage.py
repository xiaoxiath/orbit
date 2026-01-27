"""Example: Basic usage of Orbit."""

from orbit import MissionControl
from orbit.satellites import system


def main():
    """Demonstrate basic Orbit usage."""
    # Initialize Mission Control
    mission = MissionControl()

    # Register system satellites
    system_satellites = [
        system.system_get_info,
        system.system_get_clipboard,
        system.system_send_notification,
    ]
    mission.register_constellation(system_satellites)

    print("🛸 Orbit - Basic Usage Example\n")

    # Example 1: Get system information
    print("📊 Getting system information...")
    try:
        info = mission.launch("system_get_info", {})
        print(f"   macOS Version: {info['version']}")
        print(f"   Hostname: {info['hostname']}")
        print(f"   User: {info['username']}")
        print(f"   Architecture: {info['architecture']}")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 2: Send notification
    print("\n📢 Sending notification...")
    try:
        mission.launch("system_send_notification", {
            "title": "Orbit",
            "message": "Hello from Orbit! 🛸"
        })
        print("   Notification sent!")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 3: List all registered satellites
    print("\n🛰️  Registered satellites:")
    for satellite in mission.constellation.list_all():
        print(f"   - {satellite.name}: {satellite.description}")

    # Example 4: Get statistics
    print("\n📈 Constellation statistics:")
    stats = mission.constellation.get_stats()
    print(f"   Total satellites: {stats['total_satellites']}")
    print(f"   Categories: {stats['categories']}")
    print(f"   By safety level:")
    for level, count in stats['by_safety'].items():
        print(f"      {level}: {count}")


if __name__ == "__main__":
    main()
