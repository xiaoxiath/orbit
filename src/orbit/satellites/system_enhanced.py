"""Enhanced system telemetry satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser, JSONResultParser
import json

# System info satellite (enhanced)
system_get_detailed_info = Satellite(
    name="system_get_detailed_info",
    description="Get detailed macOS system information including version, hostname, hardware, memory, and disk",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        set systemVersion to system version
        set hostName to host name
        set userName to name of current user
    end tell

    tell application "Finder"
        set freeSpace to free space of startup disk
        set totalSpace to capacity of startup disk
    end tell

    set appleArchitecture to do shell script "uname -m"
    set physicalMemoryRaw to do shell script "sysctl -n hw.memsize"
    set physicalMemory to (physicalMemoryRaw / 1024 / 1024 / 1024 as string) & "GB"

    set totalGB to totalSpace / 1024 / 1024 / 1024
    set freeGB to freeSpace / 1024 / 1024 / 1024

    return systemVersion & "|" & hostName & "|" & userName & "|" & appleArchitecture & "|" & physicalMemory & "|" & (totalGB as string) & "|" & (freeGB as string)
    """,
    result_parser=DelimitedResultParser(
        delimiter="|",
        field_names=["version", "hostname", "username", "architecture", "memory", "disk_total", "disk_free"]
    ),
    examples=[
        {
            "input": {},
            "output": {
                "version": "14.0",
                "hostname": "MacBook-Pro",
                "username": "user",
                "architecture": "arm64",
                "memory": "16GB",
                "disk_total": "512.0GB",
                "disk_free": "256.5GB"
            }
        }
    ]
)

# Enhanced clipboard satellites
system_get_clipboard_history = Satellite(
    name="system_get_clipboard_history",
    description="Get clipboard and its type (text, image, file, etc.)",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        try
            set theClipboard to the clipboard as string
            set clipboardType to "text"
        on error
            try
                set theClipboard to (the clipboard as «class PNGf») as string
                set clipboardType to "image"
            on error
                set theClipboard to "unknown"
                set clipboardType to "unknown"
            end try
        end try
    end tell

    return clipboardType & "|" & theClipboard
    """,
    result_parser=DelimitedResultParser(delimiter="|", field_names=["type", "content"]),
    examples=[
        {
            "input": {},
            "output": {"type": "text", "content": "clipboard content"}
        }
    ]
)

system_clear_clipboard = Satellite(
    name="system_clear_clipboard",
    description="Clear the clipboard",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set the clipboard to ""
    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Enhanced notification satellites
system_send_notification_with_sound = Satellite(
    name="system_send_notification_with_sound",
    description="Send system notification with sound",
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
        ),
        SatelliteParameter(
            name="sound",
            type="string",
            description="Sound name (default, glass, hero, Morse, ping, pop, pulsar, sosumi, tink)",
            required=False,
            default="default",
            enum=["default", "glass", "hero", "Morse", "ping", "pop", "pulsar", "sosumi", "tink"]
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    display notification "{{ message }}" with title "{{ title }}" sound name "{{ sound }}"
    return "success"
    """,
    examples=[
        {
            "input": {"title": "Alert", "message": "Important message", "sound": "ping"},
            "output": "success"
        }
    ]
)

# Enhanced screenshot satellites
system_take_screenshot_selection = Satellite(
    name="system_take_screenshot_selection",
    description="Capture screen selection to file (interactive)",
    category="system",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Path to save screenshot",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set screenshotPath to POSIX path of "{{ path }}"
    do shell script "mkdir -p $(dirname " & quoted form of screenshotPath & ")"
    do shell script "screencapture -i " & quoted form of screenshotPath
    return screenshotPath
    """,
    examples=[
        {
            "input": {"path": "~/Desktop/selection.png"},
            "output": {"path": "/Users/user/Desktop/selection.png"}
        }
    ]
)

system_take_screenshot_window = Satellite(
    name="system_take_screenshot_window",
    description="Capture frontmost window to file",
    category="system",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Path to save screenshot",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set screenshotPath to POSIX path of "{{ path }}"
    do shell script "mkdir -p $(dirname " & quoted form of screenshotPath & ")"
    do shell script "screencapture -lw " & quoted form of screenshotPath
    return screenshotPath
    """,
    examples=[
        {
            "input": {"path": "~/Desktop/window.png"},
            "output": {"path": "/Users/user/Desktop/window.png"}
        }
    ]
)

# Enhanced volume satellites
system_mute_volume = Satellite(
    name="system_mute_volume",
    description="Mute system volume",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set volume output volume 0
    return "muted"
    """,
    examples=[
        {
            "input": {},
            "output": "muted"
        }
    ]
)

system_unmute_volume = Satellite(
    name="system_unmute_volume",
    description="Unmute system volume",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set volume output volume 50
    return "unmuted"
    """,
    examples=[
        {
            "input": {},
            "output": "unmuted"
        }
    ]
)

system_volume_up = Satellite(
    name="system_volume_up",
    description="Increase volume by one step",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set currentVolume to output volume of (get volume settings)
    set volumeUp to currentVolume + 6
    if volumeUp > 100 then set volumeUp to 100
    set volume output volume volumeUp
    return volumeUp as string
    """,
    examples=[
        {
            "input": {},
            "output": "60"
        }
    ]
)

system_volume_down = Satellite(
    name="system_volume_down",
    description="Decrease volume by one step",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set currentVolume to output volume of (get volume settings)
    set volumeDown to currentVolume - 6
    if volumeDown < 0 then set volumeDown to 0
    set volume output volume volumeDown
    return volumeDown as string
    """,
    examples=[
        {
            "input": {},
            "output": "40"
        }
    ]
)

# Enhanced brightness satellites
system_brightness_up = Satellite(
    name="system_brightness_up",
    description="Increase brightness by one step",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    try
        do shell script "brightness -l 2>/dev/null | grep brightness | awk '{print $2*100}'"
    on error
        return "50"
    end try
    """,
    examples=[
        {
            "input": {},
            "output": "85"
        }
    ]
)

system_brightness_down = Satellite(
    name="system_brightness_down",
    description="Decrease brightness by one step",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    try
        do shell script "brightness -l 2>/dev/null | grep brightness | awk '{print $2*100}'"
    on error
        return "50"
    end try
    """,
    examples=[
        {
            "input": {},
            "output": "65"
        }
    ]
)

# New: System sleep/wake satellites
system_sleep = Satellite(
    name="system_sleep",
    description="Put Mac to sleep",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "System Events" to sleep
    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

system_reboot = Satellite(
    name="system_reboot",
    description="Restart the Mac",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.CRITICAL,
    applescript_template="""
    tell application "System Events" to restart
    return "restarting"
    """,
    examples=[
        {
            "input": {},
            "output": "restarting"
        }
    ]
)

system_shutdown = Satellite(
    name="system_shutdown",
    description="Shut down the Mac",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.CRITICAL,
    applescript_template="""
    tell application "System Events" to shut down
    return "shutting down"
    """,
    examples=[
        {
            "input": {},
            "output": "shutting down"
        }
    ]
)

# Export all enhanced system satellites
__all__ = [
    # Enhanced
    "system_get_detailed_info",
    "system_get_clipboard_history",
    "system_clear_clipboard",
    "system_send_notification_with_sound",
    "system_take_screenshot_selection",
    "system_take_screenshot_window",
    "system_mute_volume",
    "system_unmute_volume",
    "system_volume_up",
    "system_volume_down",
    "system_brightness_up",
    "system_brightness_down",
    "system_sleep",
    "system_reboot",
    "system_shutdown",
]
