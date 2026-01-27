"""File communication satellites."""

from typing import Optional
from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import JSONResultParser, DelimitedResultParser
import json


# List files
file_list = Satellite(
    name="file_list",
    description="List files in a directory",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Directory path (supports ~ for home directory)",
            required=True
        ),
        SatelliteParameter(
            name="recursive",
            type="boolean",
            description="List files recursively",
            required=False,
            default=False
        ),
        SatelliteParameter(
            name="include_hidden",
            type="boolean",
            description="Include hidden files (starting with .)",
            required=False,
            default=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set folderPath to "{{ path }}"
    set recursiveFlag to {{ "true" if recursive else "false" }}
    set includeHiddenFlag to {{ "true" if include_hidden else "false" }}

    tell application "System Events"
        set fileList to {}
        set folderRef to folder folderPath

        if recursiveFlag then
            set fileRefs to every file of entire contents of folderRef
        else
            set fileRefs to every file of folderRef
        end if

        repeat with fileRef in fileRefs
            try
                set fileName to name of fileRef
                if includeHiddenFlag or (fileName does not start with ".") then
                    set filePath to POSIX path of fileRef
                    set fileType to kind of fileRef
                    set fileSize to size of fileRef
                    if (count of fileList) = 0 then
                        set end of fileList to (fileName & "|" & filePath & "|" & fileType & "|" & (fileSize as string))
                    else
                        set end of fileList to "," & (fileName & "|" & filePath & "|" & fileType & "|" & (fileSize as string))
                    end if
                end if
            end try
        end repeat
    end tell

    return fileList as string
    """,
    result_parser=lambda x: json.dumps([dict(zip(["name", "path", "type", "size"], item.split("|"))) for item in x.split(",")]),
    examples=[
        {
            "input": {"path": "~", "recursive": False},
            "output": {
                "files": [
                    {"name": "Documents", "path": "/Users/user/Documents", "type": "Folder", "size": "4096"}
                ]
            }
        }
    ]
)

# Read file
file_read = Satellite(
    name="file_read",
    description="Read file contents",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="File path to read",
            required=True
        ),
        SatelliteParameter(
            name="encoding",
            type="string",
            description="File encoding (default: utf-8)",
            required=False,
            default="utf-8"
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set filePath to POSIX path of "{{ path }}"

    tell application "System Events"
        try
            set fileContent to read (file filePath as alias) using encoding "{{ encoding }}"
            return fileContent
        on error
            return "Error: " & (error number as string)
        end try
    end tell
    """,
    examples=[
        {
            "input": {"path": "~/Documents/notes.txt"},
            "output": {"content": "File contents here..."}
        }
    ]
)

# Write file
file_write = Satellite(
    name="file_write",
    description="Write content to a file",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="File path to write",
            required=True
        ),
        SatelliteParameter(
            name="content",
            type="string",
            description="Content to write",
            required=True
        ),
        SatelliteParameter(
            name="encoding",
            type="string",
            description="File encoding (default: utf-8)",
            required=False,
            default="utf-8"
        ),
        SatelliteParameter(
            name="overwrite",
            type="boolean",
            description="Overwrite if file exists (default: true)",
            required=False,
            default=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set filePath to POSIX path of "{{ path }}"
    set fileContent to "{{ content }}"

    tell application "System Events"
        try
            set fileRef to open for access (filePath as alias) with write permission
            if {{ overwrite|lower }} then
                set eof of fileRef to 0
            end if
            write fileContent to fileRef as «class utf8» using encoding "{{ encoding }}"
            close access fileRef
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"path": "~/Documents/new_note.txt", "content": "Hello from Orbit 🛸"},
            "output": "success"
        }
    ]
)

# Delete file
file_delete = Satellite(
    name="file_delete",
    description="Delete a file",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="File path to delete",
            required=True
        )
    ],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    set filePath to POSIX path of "{{ path }}"

    tell application "Finder"
        try
            delete file filePath
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"path": "~/Desktop/test.txt"},
            "output": "success"
        }
    ]
)

# Move file
file_move = Satellite(
    name="file_move",
    description="Move a file to a new location",
    category="files",
    parameters=[
        SatelliteParameter(
            name="source",
            type="string",
            description="Source file path",
            required=True
        ),
        SatelliteParameter(
            name="destination",
            type="string",
            description="Destination path",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set sourcePath to POSIX path of "{{ source }}"
    set destPath to POSIX path of "{{ destination }}"

    tell application "Finder"
        try
            move sourcePath to destPath
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"source": "~/Desktop/file.txt", "destination": "~/Documents/"},
            "output": "success"
        }
    ]
)

# Copy file
file_copy = Satellite(
    name="file_copy",
    description="Copy a file to a new location",
    category="files",
    parameters=[
        SatelliteParameter(
            name="source",
            type="string",
            description="Source file path",
            required=True
        ),
        SatelliteParameter(
            name="destination",
            type="string",
            description="Destination path",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set sourcePath to POSIX path of "{{ source }}"
    set destPath to POSIX path of "{{ destination }}"

    tell application "Finder"
        try
            duplicate file sourcePath to (destPath as alias)
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"source": "~/Documents/file.txt", "destination": "~/Desktop/"},
            "output": "success"
        }
    ]
)

# Search files
file_search = Satellite(
    name="file_search",
    description="Search files by name in a directory",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Directory to search in",
            required=True
        ),
        SatelliteParameter(
            name="query",
            type="string",
            description="Search query (file name)",
            required=True
        ),
        SatelliteParameter(
            name="file_type",
            type="string",
            description="Filter by file extension (e.g., 'txt', 'pdf')",
            required=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set folderPath to POSIX path of "{{ path }}"
    set searchQuery to "{{ query }}"
    set results to {}

    tell application "Finder"
        set folderRef to folder folderPath
        set fileRefs to every file of entire contents of folderRef

        repeat with fileRef in fileRefs
            try
                set fileName to name of fileRef
                if fileName contains searchQuery then
                    {% if file_type %}
                    if fileName ends with ".{{ file_type }}" then
                        set end of results to (POSIX path of (fileRef as alias))
                    end if
                    {% else %}
                    set end of results to (POSIX path of (fileRef as alias))
                    {% endif %}
                end if
            end try
        end repeat
    end tell

    return (my list results) as string
    """,
    result_parser=lambda x: json.dumps(x.split(", ")) if x else json.dumps([]),
    examples=[
        {
            "input": {"path": "~", "query": "orbit", "file_type": "txt"},
            "output": {"paths": ["/Users/user/Documents/orbit.txt"]}
        }
    ]
)

# Empty trash
file_empty_trash = Satellite(
    name="file_empty_trash",
    description="Empty the trash",
    category="files",
    parameters=[],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Finder"
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

# Create directory
file_create_directory = Satellite(
    name="file_create_directory",
    description="Create a new directory",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="Directory path to create",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    set dirPath to POSIX path of "{{ path }}"

    tell application "Finder"
        try
            make new folder at (dirPath's parent) with properties {name:dirPath's last item}
            return "success"
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    examples=[
        {
            "input": {"path": "~/Documents/Orbit"},
            "output": "success"
        }
    ]
)

# Get file info
file_get_info = Satellite(
    name="file_get_info",
    description="Get file metadata",
    category="files",
    parameters=[
        SatelliteParameter(
            name="path",
            type="string",
            description="File path",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set filePath to POSIX path of "{{ path }}"

    tell application "System Events"
        try
            set fileRef to file filePath
            set fileName to name of fileRef
            set fileType to kind of fileRef
            set fileSize to size of fileRef
            set creationDate to creation date of fileRef
            set modDate to modification date of fileRef

            return fileName & "|" & fileType & "|" & (fileSize as string) & "|" & (creationDate as string) & "|" & (modDate as string)
        on error errMsg
            return "Error: " & errMsg
        end try
    end tell
    """,
    result_parser=DelimitedResultParser(
        delimiter="|",
        field_names=["name", "type", "size", "created", "modified"]
    ),
    examples=[
        {
            "input": {"path": "~/Documents/file.txt"},
            "output": {
                "name": "file.txt",
                "type": "Plain Text",
                "size": "1024",
                "created": "Monday, January 27, 2026 at 10:00:00 AM",
                "modified": "Monday, January 27, 2026 at 11:00:00 AM"
            }
        }
    ]
)

# Export all file satellites
__all__ = [
    "file_list",
    "file_read",
    "file_write",
    "file_delete",
    "file_move",
    "file_copy",
    "file_search",
    "file_empty_trash",
    "file_create_directory",
    "file_get_info",
]
