"""Example: Custom safety configuration."""

from orbit import MissionControl, SafetyShield, SafetyLevel
from orbit.satellites import system


def confirm_callback(satellite, parameters):
    """Custom confirmation callback.

    Args:
        satellite: Satellite being launched
        parameters: Mission parameters

    Returns:
        True if user confirms, False otherwise
    """
    print(f"\n⚠️  Safety Check Required")
    print(f"   Satellite: {satellite.name}")
    print(f"   Safety Level: {satellite.safety_level.value}")
    print(f"   Parameters: {parameters}")

    # For demo purposes, always return True
    # In production, you would ask the user
    return True


def main():
    """Demonstrate custom safety configuration."""
    print("🛸 Orbit - Custom Safety Configuration\n")

    # Example 1: Strict mode (only SAFE operations)
    print("1️⃣  Strict Mode (only SAFE operations):")
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
    mission_strict.register(system.system_set_clipboard)  # MODERATE

    print("   Registered satellites:")
    for sat in mission_strict.constellation.list_all():
        print(f"   - {sat.name} ({sat.safety_level.value})")

    # Example 2: Permissive mode (allow all)
    print("\n2️⃣  Permissive Mode (allow all):")
    permissive_shield = SafetyShield(
        rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "allow",
            SafetyLevel.DANGEROUS: "allow",
            SafetyLevel.CRITICAL: "allow"
        }
    )
    mission_permissive = MissionControl(safety_shield=permissive_shield)

    print("   All operations allowed without confirmation")

    # Example 3: Confirmation mode
    print("\n3️⃣  Confirmation Mode (require confirmation for MODERATE+):")
    confirm_shield = SafetyShield(
        rules={
            SafetyLevel.SAFE: "allow",
            SafetyLevel.MODERATE: "confirm",
            SafetyLevel.DANGEROUS: "confirm",
            SafetyLevel.CRITICAL: "deny"
        },
        confirmation_callback=confirm_callback
    )
    mission_confirm = MissionControl(safety_shield=confirm_shield)

    print("   MODERATE and DANGEROUS operations require confirmation")

    # Example 4: Protected paths
    print("\n4️⃣  Custom Protected Paths:")
    custom_shield = SafetyShield(
        protected_paths=[
            Path("/"),
            Path("/System"),
            Path("~/Documents"),  # Protect Documents
            Path("~/Desktop"),    # Protect Desktop
        ]
    )

    print("   Protected paths:")
    for path in custom_shield.protected_paths:
        print(f"   - {path}")


if __name__ == "__main__":
    from pathlib import Path
    main()
