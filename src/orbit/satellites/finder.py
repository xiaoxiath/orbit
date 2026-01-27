"""Finder operation satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser
import json


# Open folder in Finder
finder_open_folder = Satellite(
    name="finder_open_folder",
    description="Open folder in Finder",
    category="finder",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Folder path to open",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set folderPath to POSIX path of "{{ path }}"

    tell application "Finder"
        activate
        open folderPath
    end tell

    return "success
    """,
    examples=[
        {
            "input": {"path": "~/Documents"},
            "output": "success"
        }
    ]
)

# New folder
finder_new_folder = Satellite(
    name="finder_new_folder",
    description="Create new folder",
    category="finder",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Folder name",
            required=True
        ),
        SatelliteParameter(
            name="location",
            type="string",
            description="Parent folder path (default: Desktop)",
            required=False,
            default="~/Desktop"
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set folderPath to POSIX path of "{{ location }}"
    set folderName to "{{ name }}"

    tell application "Finder"
        make new folder at folderPath with properties {name:folderName}
    end tell

    return folderPath
    """,
    examples=[
        {
            "input": {"name": "Orbit Project", "location": "~/Documents"},
            "output": {"path": "/Users/user/Documents/Orbit Project"}
        }
    ]
)

# Reveal file in Finder
finder_reveal = Satellite(
    name="finder_reveal",
    description="Reveal file in Finder",
    category="finder",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="File path to reveal",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set filePath to POSIX path of "{{ path }}"

    tell application "Finder"
        reveal filePath
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {"path": "~/Documents/file.txt"},
            "output": "success"
        }
    ]
)

# Get selected files
finder_get_selection = Satellite(
    name="finder_get_selection",
    description="Get currently selected files in Finder",
    category="finder",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Finder"
        set selectionList to {}
        set selectedItems = selection

        repeat with selectedItem in selectedItems
            set itemPath to POSIX path of (selectedItem as alias)
            set end of selectionList to itemPath
        end repeat
    end tell

    return my list(selectionList)
    """,
    result_parser=lambda x: x.split(",") if x and x != "my list()" else [],
    examples=[
        {
            "input": {},
            "output": {"paths": ["/Users/user/Desktop/file.txt"]}
        }
    ]
)

# Empty trash
finder_empty_trash = Satellite(
    name="finder_empty_trash",
    description="Empty the trash",
    category="finder",
    parameters=[],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Finder"
        activate
        if (count of items in trash) > 0 then
            empty trash
            return "success"
        else
            return "trash is already empty"
        end if
    end tell
    """,
    examples=[
        {
            "input": {},
            "output": "success"
        }
    ]
)

# Get Trash info
finder_get_trash_info = Satellite(
    name="finder_get_trash_info",
    description="Get trash information",
    category="finder",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Finder"
        set trashCount to count of items in trash
        set trashSize = 0

        repeat with item in (every item of trash)
            try
                set trashSize to trashSize + (physical size of item)
            end try
        end repeat

        return trashCount & "|" & (trashSize as string)
    """,
    result_parser=DelimitedResultParser(delimiter="|", field_names=["count", "size"]),
    examples=[
        {
            "input": {},
            "output": {"count": "5", "size": "1024000"}
        }
    ]
)

# Export all finder satellites
__all__ = [
    "finder_open_folder",
    "finder_new_folder",
    "finder_reveal",
    "finder_get_selection",
    "finder_empty_trash",
    "finder_get_trash_info",
]
