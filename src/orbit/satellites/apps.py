"""Application control satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser, JSONResultParser
import json


# List applications
app_list = Satellite(
    name="app_list",
    description="List installed applications",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Path to search (default: /Applications)",
            required=False,
            default="/Applications"
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set searchPath to POSIX path of "{{ path }}"

    tell application "System Events"
        set appList to {}
        set allApps to every application process

        repeat with appProcess in allApps
            try
                set appName to name of appProcess
                if appName is not background only then
                    set appPath to POSIX path of (application file of appProcess)
                    if appPath starts with searchPath then
                        set end of appList to appName
                    end if
                end if
            end try
        end repeat
    end tell

    return my list(appList)
    """,
    result_parser=lambda x: sorted(x.split(",") if x else []),
    examples=[
        {
            "input": {},
            "output": {"apps": ["Safari", "Notes", "Calendar", "Mail"]}
        }
    ]
)

# Launch application
app_launch = Satellite(
    name="app_launch",
    description="Launch application",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "{{ name }}"
        activate
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Safari"},
            "output": "success"
        }
    ]
)

# Quit application
app_quit = Satellite(
    name="app_quit",
    description="Quit application",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "{{ name }}"
        quit
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Music"},
            "output": "success"
        }
    ]
)

# Activate application
app_activate = Satellite(
    name="app_activate",
    description="Bring application to front",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "{{ name }}"
        activate
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Safari"},
            "output": "success"
        }
    ]
)

# Get running applications
app_get_running = Satellite(
    name="app_get_running",
    description="Get list of running applications",
    category="apps",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        set runningApps = {}
        set allProcesses to every process

        repeat with currentProcess in allProcesses
            try
                set appName to name of currentProcess
                if background only of currentProcess is false then
                    set end of runningApps to appName
                end if
            end try
        end repeat
    end tell

    return my list(runningApps)
    """,
    result_parser=lambda x: sorted(x.split(",") if x and x != "my list()" else []),
    examples=[
        {
            "input": {},
            "output": {"apps": ["Finder", "Safari", "Music"]}
        }
    ]
)

# Force quit application
app_force_quit = Satellite(
    name="app_force_quit",
    description="Force quit application",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "{{ name }}"
    quit
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Calculator"},
            "output": "success"
        }
    ]
)

# Hide application
app_hide = Satellite(
    name="app_hide",
    description="Hide application",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "{{ name }}"
    activate
    tell application "System Events"
        set visible of process (first process whose name is "{{ name }}") to false
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Safari"},
            "output": "success"
        }
    ]
)

# Show application
app_show = Satellite(
    name="app_show",
    description="Show hidden application",
    category="apps",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Application name",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "{{ name }}"
    activate
    tell application "System Events"
        set visible of process (first process whose name is "{{ name }}") to true
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"name": "Safari"},
            "output": "success"
        }
    ]
)

# Export all app satellites
__all__ = [
    "app_list",
    "app_launch",
    "app_quit",
    "app_activate",
    "app_get_running",
    "app_force_quit",
    "app_hide",
    "app_show",
]
