"""Reminders station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser
from datetime import datetime


# List reminders
reminders_list = Satellite(
    name="reminders_list",
    description="List all reminders",
    category="reminders",
    parameters=[
        SatelliteParameter(
            name="list_name",
            type="string",
            description="List name (default: all reminders)",
            required=False
        ),
        SatelliteParameter(
            name="include_completed",
            type="boolean",
            description="Include completed reminders",
            required=False,
            default=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Reminders"
        set reminderList to {}

        {% if list_name %}
        set targetList to first list whose name is "{{ list_name }}"
        {% if include_completed|lower %}
        set allReminders to every reminder in targetList
        {% else %}
        set allReminders to every reminder in targetList whose completed is false
        {% endif %}
        {% else %}
        {% if include_completed|lower %}
        set allReminders to every reminder
        {% else %}
        set allReminders to every reminder whose completed is false
        {% endif %}
        {% endif %}

        repeat with currentReminder in allReminders
            set reminderName to name of currentReminder
            set reminderDue to due date of currentReminder
            set isCompleted to completed of currentReminder as string
            set reminderId to id of currentReminder
            if (count of reminderList) = 0 then
                set end of reminderList to (reminderName & "|" & reminderDue & "|" & isCompleted & "|" & reminderId)
            else
                set end of reminderList to "," & (reminderName & "|" & reminderDue & "|" & isCompleted & "|" & reminderId)
            end if
        end repeat
    end tell

    return reminderList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "due_date", "completed", "id"], item.split("|", 3))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {"include_completed": False},
            "output": {
                "reminders": [
                    {"name": "Meeting", "due_date": "2026-01-28", "completed": "false", "id": "..."}
                ]
            }
        }
    ]
)

# Create reminder
reminders_create = Satellite(
    name="reminders_create",
    description="Create a new reminder",
    category="reminders",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Reminder name",
            required=True
        ),
        SatelliteParameter(
            name="due_date",
            type="string",
            description="Due date (format: YYYY-MM-DD HH:MM)",
            required=False
        ),
        SatelliteParameter(
            name="list_name",
            type="string",
            description="List name (default: first list)",
            required=False,
            default="Reminders"
        ),
        SatelliteParameter(
            name="priority",
            type="integer",
            description="Priority (0: none, 1: low, 5: medium, 9: high)",
            required=False,
            default=0,
            enum=[0, 1, 5, 9]
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Reminders"
        set targetList to first list whose name is "{{ list_name }}"

        tell targetList
            set newReminder to make new reminder with properties {name:"{{ name }}"}
            {% if due_date %}
            set due date of newReminder to date "{{ due_date }}"
            {% endif %}
            {% if priority > 0 %}
            set priority of newReminder to {{ priority }}
            {% endif %}
        end tell

        return "success"
    end tell
    """,
    examples=[
        {
            "input": {"name": "Team meeting", "due_date": "2026-01-28 15:00", "priority": 5},
            "output": "success"
        }
    ]
)

# Complete reminder
reminders_complete = Satellite(
    name="reminders_complete",
    description="Mark reminder as completed",
    category="reminders",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Reminder name to complete",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Reminders"
        set targetReminder to first reminder whose name is "{{ name }}"

        if targetReminder exists then
            set completed of targetReminder to true
            return "success"
        else
            return "Error: Reminder not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"name": "Team meeting"},
            "output": "success"
        }
    ]
)

# Uncomplete reminder
reminders_uncomplete = Satellite(
    name="reminders_uncomplete",
    description="Mark reminder as incomplete",
    category="reminders",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Reminder name to uncomplete",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Reminders"
        set targetReminder to first reminder whose name is "{{ name }}"

        if targetReminder exists then
            set completed of targetReminder to false
            return "success"
        else
            return "Error: Reminder not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"name": "Team meeting"},
            "output": "success"
        }
    ]
)

# Delete reminder
reminders_delete = Satellite(
    name="reminders_delete",
    description="Delete a reminder",
    category="reminders",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Reminder name to delete",
            required=True
        )
    ],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Reminders"
        set targetReminder to first reminder whose name is "{{ name }}"

        if targetReminder exists then
            delete targetReminder
            return "success"
        else
            return "Error: Reminder not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"name": "Old reminder"},
            "output": "success"
        }
    ]
)

# List reminder lists
reminders_list_lists = Satellite(
    name="reminders_list_lists",
    description="List all reminder lists",
    category="reminders",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Reminders"
        set listList to {}
        set allLists to every list

        repeat with currentList in allLists
            set listName to name of currentList
            set listCount to count of reminders of currentList
            if (count of listList) = 0 then
                set end of listList to (listName & "|" & (listCount as string))
            else
                set end of listList to "," & (listName & "|" & (listCount as string))
            end if
        end repeat
    end tell

    return listList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "count"], item.split("|"))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {},
            "output": {
                "lists": [
                    {"name": "Reminders", "count": "5"},
                    {"name": "Work", "count": "3"}
                ]
            }
        }
    ]
)

# Export all reminders satellites
__all__ = [
    "reminders_list",
    "reminders_create",
    "reminders_complete",
    "reminders_uncomplete",
    "reminders_delete",
    "reminders_list_lists",
]
