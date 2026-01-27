# Orbit Security Model

> **Version:** 1.0
> **Last Updated:** 2026-01-27

---

## 🛡️ Overview

Orbit's security model is designed to protect your Mac while enabling powerful automation. The **Shield System** provides multi-layered safety controls without requiring explicit approval for every operation.

---

## 🔐 Security Architecture

### 4-Tier Safety System

Every satellite is classified into one of four safety levels:

| Level | Description | Examples | Default Action |
|-------|-------------|----------|----------------|
| **SAFE** | Read-only operations, no side effects | Get system info, read clipboard, list files | ✅ Allow |
| **MODERATE** | Create/modify operations, data changes | Create note, set clipboard, write file | ⚠️ Confirm |
| **DANGEROUS** | Delete operations, irreversible | Delete file, empty trash, delete note | ⚠️ Confirm |
| **CRITICAL** | System-level operations | Terminal execution, system file modification | 🚫 Deny |

### Safety Classifications by Category

```
System Telemetry:
  └─ Most operations: SAFE
  └─ System changes: MODERATE

File Communications:
  ├─ Read operations: SAFE
  ├─ Write operations: MODERATE
  └─ Delete operations: DANGEROUS

App Stations:
  ├─ Read/list: SAFE
  ├─ Create/update: MODERATE
  └─ Delete: DANGEROUS

Network:
  └─ All operations: MODERATE

Application Control:
  ├─ List: SAFE
  └─ Launch/quit: MODERATE
```

---

## 🚦 Shield Configuration

### Default Behavior

```python
from orbit import MissionControl

# Uses default shield configuration
mission = MissionControl()

# Default rules:
# SAFE       -> allow
# MODERATE   -> require_confirmation
# DANGEROUS  -> require_confirmation
# CRITICAL   -> deny
```

### Custom Rules

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# Strict mode: block anything not SAFE
strict_shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "deny",
        SafetyLevel.DANGEROUS: "deny",
        SafetyLevel.CRITICAL: "deny"
    }
)

mission = MissionControl(safety_shield=strict_shield)
```

### Permissive Mode (Development Only)

```python
# Allow everything (NOT recommended for production)
permissive_shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "allow",
        SafetyLevel.DANGEROUS: "allow",
        SafetyLevel.CRITICAL: "allow"
    }
)

mission = MissionControl(safety_shield=permissive_shield)
```

---

## ✅ User Confirmation

### Built-in Confirmation Callback

```python
from orbit import SafetyShield

def confirm_mission(satellite, parameters):
    """Interactive confirmation prompt"""
    print(f"\n{'='*60}")
    print(f"🛰️  Satellite: {satellite.name}")
    print(f"📋 Description: {satellite.description}")
    print(f"⚠️  Safety Level: {satellite.safety_level.value}")
    print(f"📝 Parameters:")
    for key, value in parameters.items():
        print(f"   - {key}: {value}")
    print(f"{'='*60}")

    response = input("Allow this mission? (y/n): ").lower().strip()
    return response == 'y'

shield = SafetyShield(
    confirmation_callback=confirm_mission
)
```

### Programmatic Confirmation

```python
def auto_approve_safe(satellite, parameters):
    """Auto-approve SAFE level, confirm others"""
    if satellite.safety_level == SafetyLevel.SAFE:
        return True
    return ask_user(satellite, parameters)

shield = SafetyShield(confirmation_callback=auto_approve_safe)
```

### GUI Confirmation (Advanced)

```python
import tkinter as tk
from tkinter import messagebox

def gui_confirmation(satellite, parameters):
    """Show GUI confirmation dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide main window

    title = f"Orbit Shield - {satellite.safety_level.value.upper()}"
    message = f"Allow satellite '{satellite.name}'?\n\nParameters:\n"
    for key, value in parameters.items():
        message += f"  {key}: {value}\n"

    result = messagebox.askyesno(title, message)
    root.destroy()
    return result

shield = SafetyShield(confirmation_callback=gui_confirmation)
```

---

## 🚫 Protected Resources

### Default Protected Paths

The following paths are protected by default:

```python
PROTECTED_PATHS = [
    "/",              # Root directory
    "/System",        # System files
    "/Library",       # Library directories
    "/usr",           # Unix utilities
    "/bin",           # Binaries
    "/sbin",          # System binaries
    "/etc",           # Configuration files
]
```

### Custom Protected Paths

```python
from pathlib import Path
from orbit import SafetyShield

shield = SafetyShield(
    protected_paths=[
        Path("/"),
        Path("/System"),
        Path("/Library"),
        Path("/usr"),
        Path("~/Documents"),      # Protect documents
        Path("~/Desktop"),        # Protect desktop
        Path("~/Pictures"),       # Protect pictures
    ]
)
```

### Add/Remove Protected Paths

```python
shield = SafetyShield()

# Add additional protection
shield.add_protected_path("~/Projects")
shield.add_protected_path("~/Important")

# Remove protection (use with caution)
shield.remove_protected_path("~/Desktop")
```

---

## ⚠️ Dangerous Command Detection

### Default Blocked Commands

```python
DANGEROUS_COMMANDS = [
    "rm -rf /",            # Delete root
    "dd if=/dev/zero",     # Disk wipe
    ":(){ :|:& };:",       # Fork bomb
    "mkfs",                # Format filesystem
    "chmod 000",           # Remove permissions
    "chown root",          # Change ownership to root
    "mv / System",         # Move system directory
]
```

### Custom Dangerous Patterns

```python
shield = SafetyShield(
    dangerous_commands=[
        "rm -rf",
        "dd if=/dev/zero",
        "mkfs",
        "chmod 000",
        "format",
        "del /Q",          # Windows
        "rmdir /S",        # Windows
    ]
)
```

---

## 🔒 Permission Requirements

### macOS Permissions

Orbit requires various macOS permissions depending on the satellites used:

#### Accessibility (Required)

**Required for:** Application control, system-wide operations

**How to enable:**
```
System Settings → Privacy & Security → Accessibility
→ Add Terminal / Python / Your IDE
```

#### Full Disk Access (Optional)

**Required for:** Accessing all files (including system files)

**How to enable:**
```
System Settings → Privacy & Security → Full Disk Access
→ Add Terminal / Python
```

#### Automation (App-Specific)

**Required for:** Controlling specific applications

**How to enable:**
```
System Settings → Privacy & Security → Automation
→ Allow Terminal to control:
  - Notes
  - Calendar
  - Reminders
  - Music
  - etc.
```

### Check Permissions

```python
from orbit import MissionControl

mission = MissionControl()

# Check if required permissions are granted
permissions = mission.check_permissions()

for permission, granted in permissions.items():
    status = "✅ Granted" if granted else "❌ Missing"
    print(f"{permission}: {status}")
```

---

## 🚨 Security Best Practices

### 1. Never Disable the Shield

```python
# ❌ BAD: Disabling safety
result = mission.launch("dangerous_operation", {...}, bypass_shield=True)

# ✅ GOOD: Keep shield enabled
result = mission.launch("dangerous_operation", {...})
```

### 2. Use Confirmation for Production

```python
# ✅ GOOD: Always confirm in production
shield = SafetyShield(
    confirmation_callback=production_confirmation_callback
)
```

### 3. Whitelist Approved Operations

```python
# ✅ GOOD: Only register safe satellites
from orbit.satellites import system_satellites

mission = MissionControl()
for satellite in system_satellites:
    if satellite.safety_level == SafetyLevel.SAFE:
        mission.register(satellite)
```

### 4. Audit Mission Logs

```python
import logging
from orbit import MissionControl

# Enable logging
logging.basicConfig(level=logging.INFO)
mission = MissionControl()

# All missions are logged
mission.launch("notes_create", {...})
# Output: INFO:orbit.launcher:Launched mission 'notes_create' with parameters {...}
```

### 5. Validate Parameters

```python
from orbit import MissionControl

def validate_parameters(satellite, parameters):
    """Custom parameter validation"""
    if satellite.name == "file_delete":
        path = parameters.get("path", "")
        if path.startswith("/System"):
            raise ValueError("Cannot delete system files")
    return True

shield = SafetyShield(
    pre_validator=validate_parameters
)
```

---

## 🔄 Security Audit

### View Satellite Classifications

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# Group by safety level
for level in ["safe", "moderate", "dangerous", "critical"]:
    satellites = mission.constellation.list_by_safety(
        SafetyLevel[level.upper()]
    )
    print(f"\n{level.upper()} ({len(satellites)} satellites):")
    for sat in satellites:
        print(f"  - {sat.name}")
```

### Security Report

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# Generate security report
report = mission.constellation.get_stats()

print("Orbit Security Report")
print("=" * 60)
print(f"Total Satellites: {report['total_satellites']}")
print(f"Categories: {report['categories']}")
print("\nBy Safety Level:")
for level, count in report['by_safety'].items():
    print(f"  {level}: {count}")
```

---

## 🐛 Security Testing

### Test Shield Behavior

```python
import pytest
from orbit import SafetyShield, SafetyLevel
from orbit.core.exceptions import ShieldError

def test_protected_path_blocking():
    shield = SafetyShield()

    # Attempt to access protected path
    with pytest.raises(ShieldError):
        shield._check_path("/System")

def test_dangerous_command_blocking():
    shield = SafetyShield()

    # Attempt to execute dangerous command
    with pytest.raises(ShieldError):
        shield._check_command("rm -rf /")

def test_safety_level_enforcement():
    from orbit.satellites import Satellite

    # Create CRITICAL satellite
    critical_sat = Satellite(
        name="critical_operation",
        description="Critical test",
        category="test",
        parameters=[],
        safety_level=SafetyLevel.CRITICAL,
        applescript_template=""
    )

    shield = SafetyShield()  # CRITICAL -> DENY by default

    with pytest.raises(ShieldError):
        shield.validate(critical_sat, {})
```

---

## 📖 References

- [Shield API Reference](API_REFERENCE.md#shield)
- [Exception Handling](API_REFERENCE.md#exceptions)
- [Permission Setup Guide](TROUBLESHOOTING.md#permissions)
- [Security Best Practices](https://owasp.org/

---

**Security Model Version:** 1.0
**Last Updated:** 2026-01-27

🛡️ Stay safe, orbit safely!
