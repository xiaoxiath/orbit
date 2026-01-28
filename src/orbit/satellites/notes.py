"""Notes station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser


# List notes
notes_list = Satellite(
    name="notes_list",
    description="List all notes in a folder",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder name (default: first folder if not specified)",
            required=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Notes"
        set noteList to {}
        {% if folder %}
        set targetFolder to first folder whose name is "{{ folder }}"
        {% else %}
        set targetFolder to first folder
        {% endif %}

        if targetFolder exists then
            set allNotes to every note in targetFolder
            repeat with currentNote in allNotes
                set noteName to name of currentNote
                set noteBody to body of currentNote
                set noteId to id of currentNote
                if (count of noteList) = 0 then
                    set end of noteList to (noteName & "|" & noteBody & "|" & noteId)
                else
                    set end of noteList to "," & (noteName & "|" & noteBody & "|" & noteId)
                end if
            end repeat
        end if
    end tell

    return noteList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "body", "id"], note.split("|", 2))) for note in x.split(",")],
    examples=[
        {
            "input": {"folder": "Notes"},
            "output": {
                "notes": [
                    {"name": "Meeting Notes", "body": "Discussion points...", "id": "x-coredata://..."}
                ]
            }
        }
    ]
)

# Get note
notes_get = Satellite(
    name="notes_get",
    description="Get note content by name",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Note name",
            required=True
        ),
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder name (default: first folder)",
            required=False,
            default="Notes"
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Notes"
        set targetFolder to first folder whose name is "{{ folder }}"
        set targetNote to first note of targetFolder whose name is "{{ name }}"

        if targetNote exists then
            set noteBody to body of targetNote
            set noteCreationDate to creation date of targetNote
            set noteModDate = modification date of targetNote
            return noteBody & "|" & (noteCreationDate as string) & "|" & (noteModDate as string)
        else
            return "Error: Note not found"
        end if
    end tell
    """,
    result_parser=DelimitedResultParser(
        delimiter="|",
        field_names=["body", "created", "modified"]
    ),
    examples=[
        {
            "input": {"name": "Meeting Notes"},
            "output": {
                "body": "Discussion points...",
                "created": "Monday, January 27, 2026",
                "modified": "Monday, January 27, 2026"
            }
        }
    ]
)

# Create note
notes_create = Satellite(
    name="notes_create",
    description="Create a new note",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="title",
            type="string",
            description="Note title",
            required=True
        ),
        SatelliteParameter(
            name="body",
            type="string",
            description="Note content (supports HTML)",
            required=True
        ),
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder name (default: first folder if not specified)",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Notes"
        {% if folder %}
        set targetFolder to first folder whose name is "{{ folder }}"
        {% else %}
        set targetFolder to first folder
        {% endif %}
        tell targetFolder
            make new note with properties {name:"{{ title }}", body:"{{ body }}"}
        end tell
        return "success"
    end tell
    """,
    examples=[
        {
            "input": {
                "title": "Shopping List",
                "body": "<h1>Shopping</h1><ul><li>Milk</li><li>Eggs</li></ul>",
                "folder": "Notes"
            },
            "output": "success"
        }
    ]
)

# Update note
notes_update = Satellite(
    name="notes_update",
    description="Update an existing note",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Note name to update",
            required=True
        ),
        SatelliteParameter(
            name="body",
            type="string",
            description="New note content",
            required=True
        ),
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder name (default: first folder if not specified)",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Notes"
        {% if folder %}
        set targetFolder to first folder whose name is "{{ folder }}"
        {% else %}
        set targetFolder to first folder
        {% endif %}
        set targetNote to first note of targetFolder whose name is "{{ name }}"

        if targetNote exists then
            set body of targetNote to "{{ body }}"
            return "success"
        else
            return "Error: Note not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"name": "Meeting Notes", "body": "Updated content..."},
            "output": "success"
        }
    ]
)

# Delete note
notes_delete = Satellite(
    name="notes_delete",
    description="Delete a note",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Note name to delete",
            required=True
        ),
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder name (default: first folder if not specified)",
            required=False
        )
    ],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Notes"
        {% if folder %}
        set targetFolder to first folder whose name is "{{ folder }}"
        {% else %}
        set targetFolder to first folder
        {% endif %}
        set targetNote to first note of targetFolder whose name is "{{ name }}""

        if targetNote exists then
            delete targetNote
            return "success"
        else
            return "Error: Note not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"name": "Old Note"},
            "output": "success"
        }
    ]
)

# Search notes
notes_search = Satellite(
    name="notes_search",
    description="Search notes by query",
    category="notes",
    parameters=[
        SatelliteParameter(
            name="query",
            type="string",
            description="Search query",
            required=True
        ),
        SatelliteParameter(
            name="folder",
            type="string",
            description="Folder to search in (default: all folders)",
            required=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Notes"
        set results to {}

        {% if folder %}
        set targetFolder to first folder whose name is "{{ folder }}"
        set allNotes to every note in targetFolder
        {% else %}
        set allNotes to every note
        {% endif %}

        repeat with currentNote in allNotes
            set noteName to name of currentNote
            set noteBody to body of currentNote

            if noteName contains "{{ query }}" or noteBody contains "{{ query }}" then
                if (count of results) = 0 then
                    set end of results to (noteName & "|" & (name of container of currentNote))
                else
                    set end of results to "," & (noteName & "|" & (name of container of currentNote))
                end if
            end if
        end repeat
    end tell

    return results as string
    """,
    result_parser=lambda x: [dict(zip(["name", "folder"], item.split("|"))) for item in x.split(",")],
    examples=[
        {
            "input": {"query": "meeting"},
            "output": {
                "results": [
                    {"name": "Meeting Notes", "folder": "Work"}
                ]
            }
        }
    ]
)

# List folders
notes_list_folders = Satellite(
    name="notes_list_folders",
    description="List all note folders",
    category="notes",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Notes"
        set folderList to {}
        set allFolders to every folder

        repeat with currentFolder in allFolders
            set folderName to name of currentFolder
            if (count of folderList) = 0 then
                set end of folderList to folderName
            else
                set end of folderList to "," & folderName
            end if
        end repeat
    end tell

    return folderList as string
    """,
    result_parser=lambda x: x.split(",") if x else [],
    examples=[
        {
            "input": {},
            "output": {"folders": ["Notes", "Work", "Personal"]}
        }
    ]
)

# Export all notes satellites
__all__ = [
    "notes_list",
    "notes_get",
    "notes_create",
    "notes_update",
    "notes_delete",
    "notes_search",
    "notes_list_folders",
]
