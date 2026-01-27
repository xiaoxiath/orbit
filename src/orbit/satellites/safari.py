"""Safari station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser


# Open URL
safari_open = Satellite(
    name="safari_open",
    description="Open URL in Safari",
    category="safari",
    parameters=[
        SatelliteParameter(
            name="url",
            type="string",
            description="URL to open",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        open location "{{ url }}" in current tab of front window
    end tell
    return "success"
    """,
    examples=[
        {
            "input": {"url": "https://github.com"},
            "output": "success"
        }
    ]
)

# Get current URL
safari_get_url = Satellite(
    name="safari_get_url",
    description="Get current tab URL",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        tell front document
            set currentURL to URL
        end tell
    end tell
    return currentURL
    """,
    examples=[
        {
            "input": {},
            "output": {"url": "https://github.com"}
        }
    ]
)

# Get page text
safari_get_text = Satellite(
    name="safari_get_text",
    description="Get current page text content",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        tell front document
            if (do JavaScript "document.body.innerText" in front document) then
                set pageText to (do JavaScript "document.body.innerText" in front document)
            else
                set pageText to ""
            end if
        end tell
    end tell

    return pageText
    """,
    examples=[
        {
            "input": {},
            "output": {"text": "Page text content..."}
        }
    ]
)

# List tabs
safari_list_tabs = Satellite(
    name="safari_list_tabs",
    description="List all open tabs",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        set tabList to {}
        set windowCount to count of windows

        repeat with i from 1 to windowCount
            set currentWindow to window i
            set tabCount to count of tabs of currentWindow

            repeat with j from 1 to tabCount
                set currentTab to tab j of currentWindow
                set tabName to name of currentTab
                set tabURL to URL of currentTab

                set end of tabList to (tabName & "|" & tabURL)
            end repeat
        end repeat
    end tell

    return my list(tabList)
    """,
    result_parser=lambda x: [dict(zip(["name", "url"], item.split("|", 1))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {},
            "output": {
                "tabs": [
                    {"name": "GitHub", "url": "https://github.com"}
                ]
            }
        }
    ]
)

# Close tab
safari_close_tab = Satellite(
    name="safari_close_tab",
    description="Close current tab",
    category="safari",
    parameters=[
        SatelliteParameter(
            name="index",
            type="integer",
            description="Tab index to close (1-based, default: current tab)",
            required=False,
            default=0
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Safari"
        {% if index == 0 %}
        close current tab
        {% else %}
        close tab {{ index }}
        {% endif %}
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"index": 2},
            "output": "success"
        }
    ]
)

# Search web
safari_search = Satellite(
    name="safari_search",
    description="Search web in Safari",
    category="safari",
    parameters=[
        SatelliteParameter(
            name="query",
            type="string",
            description="Search query",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        set searchURL to "https://www.google.com/search?q={{ query }}"
        open location searchURL in current tab of front window
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"query": "Orbit macOS automation"},
            "output": "success"
        }
    ]
)

# New tab
safari_new_tab = Satellite(
    name="safari_new_tab",
    description="Open new tab",
    category="safari",
    parameters=[
        SatelliteParameter(
            name="url",
            type="string",
            description="URL to open (optional)",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Safari"
        activate
        {% if url %}
        open location "{{ url }}" in new tab
        {% else %}
        make new document
        {% endif %}
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"url": "https://github.com"},
            "output": "success"
        }
    ]
)

# Go back
safari_go_back = Satellite(
    name="safari_go_back",
    description="Go back in history",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        tell application "System Events"
            keystroke "[" using {command down}
        end tell
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Go forward
safari_go_forward = Satellite(
    name="safari_go_forward",
    description="Go forward in history",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        tell application "System Events"
            keystroke "]" using {command down}
        end tell
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Refresh page
safari_refresh = Satellite(
    name="safari_refresh",
    description="Refresh current page",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        tell application "System Events"
            keystroke "r" using {command down}
        end tell
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Zoom in/out
safari_zoom_in = Satellite(
    name="safari_zoom_in",
    description="Zoom in page",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        tell application "System Events"
            keystroke "+" using {command down}
        end tell
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

safari_zoom_out = Satellite(
    name="safari_zoom_out",
    description="Zoom out page",
    category="safari",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Safari"
        activate
        tell application "System Events"
            keystroke "-" using {command down}
        end tell
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Export all safari satellites
__all__ = [
    "safari_open",
    "safari_get_url",
    "safari_get_text",
    "safari_list_tabs",
    "safari_close_tab",
    "safari_search",
    "safari_new_tab",
    "safari_go_back",
    "safari_go_forward",
    "safari_refresh",
    "safari_zoom_in",
    "safari_zoom_out",
]
