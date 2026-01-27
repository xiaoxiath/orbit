"""System telemetry satellites."""

from typing import Optional
from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser

# System info satellite
system_get_info = Satellite(
    name="system_get_info",
    description="Get macOS system information including version, hostname, and hardware details",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set systemInfo to do shell script "sw_vers -productVersion"
    set hostInfo to do shell script "hostname"
    set userInfo to do shell script "whoami"
    set archInfo to do shell script "uname -m"

    return systemInfo & "|" & hostInfo & "|" & userInfo & "|" & archInfo
    """,
    result_parser=DelimitedResultParser(
        delimiter="|", field_names=["version", "hostname", "username", "architecture"]
    ),
    examples=[
        {
            "input": {},
            "output": {
                "version": "14.0",
                "hostname": "MacBook-Pro",
                "username": "user",
                "architecture": "arm64"
            }
        }
    ]
)

# Clipboard satellites
system_get_clipboard = Satellite(
    name="system_get_clipboard",
    description="Read current clipboard contents",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set theClipboard to the clipboard as string
    return theClipboard
    """,
    examples=[
        {
            "input": {},
            "output": {"content": "clipboard text"}
        }
    ]
)

system_set_clipboard = Satellite(
    name="system_set_clipboard",
    description="Set clipboard contents",
    category="system",
    parameters=[
        SatelliteParameter(
            name="content",
            type="string",
            description="Content to set in clipboard",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set the clipboard to "{{ content }}" as string
    return "success"
    """,
    examples=[
        {
            "input": {"content": "Hello from Orbit 🛸"},
            "output": "success"
        }
    ]
)

# Notification satellite
system_send_notification = Satellite(
    name="system_send_notification",
    description="Send system notification",
    category="system",
    parameters=[
        SatelliteParameter(
            name="title",
            type="string",
            description="Notification title",
            required=True
        ),
        SatelliteParameter(
            name="message",
            type="string",
            description="Notification message",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    display notification "{{ message }}" with title "{{ title }}"
    return "success"
    """,
    examples=[
        {
            "input": {"title": "Orbit", "message": "Mission accomplished!"},
            "output": "success"
        }
    ]
)

# Screenshot satellite
system_take_screenshot = Satellite(
    name="system_take_screenshot",
    description="Capture screen to file",
    category="system",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Path to save screenshot (supports ~ for home directory)",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set screenshotPath to POSIX path of "{{ path }}"
    do shell script "mkdir -p $(dirname " & quoted form of screenshotPath & ")"
    do shell script "screencapture -x " & quoted form of screenshotPath
    return screenshotPath
    """,
    examples=[
        {
            "input": {"path": "~/Desktop/screenshot.png"},
            "output": {"path": "/Users/user/Desktop/screenshot.png"}
        }
    ]
)

# Volume satellites
system_get_volume = Satellite(
    name="system_get_volume",
    description="Get current system volume level (0-100)",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        set volumeLevel to output volume of (get volume settings)
    end tell
    return volumeLevel
    """,
    examples=[
        {
            "input": {},
            "output": {"volume": 50}
        }
    ]
)

system_set_volume = Satellite(
    name="system_set_volume",
    description="Set system volume level (0-100)",
    category="system",
    parameters=[
        SatelliteParameter(
            name="level",
            type="integer",
            description="Volume level (0-100)",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set volume {{ level }}
    return "{{ level }}"
    """,
    examples=[
        {
            "input": {"level": 50},
            "output": "50"
        }
    ]
)

# Brightness satellites (Note: brightness control may require permissions)
system_get_brightness = Satellite(
    name="system_get_brightness",
    description="Get screen brightness level (0-100)",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        try
            set brightnessLevel to brightness of (get display settings)
        on error
            set brightnessLevel to 50
        end try
    end tell
    return brightnessLevel
    """,
    examples=[
        {
            "input": {},
            "output": {"brightness": 75}
        }
    ]
)

system_set_brightness = Satellite(
    name="system_set_brightness",
    description="Set screen brightness level (0-100)",
    category="system",
    parameters=[
        SatelliteParameter(
            name="level",
            type="integer",
            description="Brightness level (0-100)",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "System Events"
        set brightness to {{ level }}
    end tell
    return "{{ level }}"
    """,
    examples=[
        {
            "input": {"level": 75},
            "output": "75"
        }
    ]
)

# Export all system satellites
__all__ = [
    "system_get_info",
    "system_get_clipboard",
    "system_set_clipboard",
    "system_send_notification",
    "system_take_screenshot",
    "system_get_volume",
    "system_set_volume",
    "system_get_brightness",
    "system_set_brightness",
]
