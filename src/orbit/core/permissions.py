"""Permission checking and helpful error messages for Orbit."""

from typing import Optional


def get_permission_hint(error_message: str, satellite_name: str) -> Optional[str]:
    """
    Get helpful permission hint based on error message and satellite name.

    Args:
        error_message: The error message from AppleScript
        satellite_name: Name of the satellite being executed

    Returns:
        Helpful hint message or None
    """
    error_lower = error_message.lower()

    # Safari automation permissions
    if "safari" in satellite_name.lower() or "不允许访问" in error_message or "not allowed" in error_lower:
        return """
🔐 Safari Automation Permission Required:

To use Safari automation, you need to grant permissions:

1. Open System Settings (系统设置)
2. Go to Privacy & Security (隐私与安全性)
3. Go to Automation (自动化)
4. Find Terminal (终端) or your IDE
5. Enable Safari (Safari 浏览器) in the list

Then try again.
"""

    # System Events permissions
    if "system events" in error_lower or "system events" in error_message:
        return """
🔐 System Events Permission Required:

To use system automation, you need to grant permissions:

1. Open System Settings (系统设置)
2. Go to Privacy & Security (隐私与安全性)
3. Go to Accessibility (辅助功能)
4. Add Terminal (终端) or your IDE to the list
5. Enable the checkbox

Then try again.
"""

    # Finder permissions
    if "finder" in satellite_name.lower() and "finder" in error_lower:
        return """
🔐 Finder Permission Required:

To use Finder automation, you need to grant permissions:

1. Open System Settings (系统设置)
2. Go to Privacy & Security (隐私与安全性)
3. Go to Accessibility (辅助功能)
4. Add Terminal (终端) or your IDE to the list
5. Enable the checkbox

Then try again.
"""

    # File access permissions
    if "file_" in satellite_name.lower() and ("access" in error_lower or "permission" in error_lower):
        return """
🔐 File Access Permission Required:

To access files, you may need to grant Full Disk Access:

1. Open System Settings (系统设置)
2. Go to Privacy & Security (隐私与安全性)
3. Go to Full Disk Access (完全磁盘访问权限)
4. Add Terminal (终端) or your IDE to the list
5. Enable the checkbox

Then try again.
"""

    return None


def format_error_with_hint(error_message: str, satellite_name: str) -> str:
    """
    Format error message with helpful permission hints.

    Args:
        error_message: The error message
        satellite_name: Name of the satellite

    Returns:
        Formatted error message with hints
    """
    hint = get_permission_hint(error_message, satellite_name)

    output = f"❌ Error: {error_message}"

    if hint:
        output += f"\n{hint}\n"

    return output
