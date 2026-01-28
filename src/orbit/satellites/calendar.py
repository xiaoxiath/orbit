"""Calendar station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser
import json


# List calendars
calendar_list_calendars = Satellite(
    name="calendar_list_calendars",
    description="List all calendars",
    category="calendar",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Calendar"
        set calendarList to {}
        set allCalendars to every calendar

        repeat with currentCalendar in allCalendars
            set calendarName to name of currentCalendar
            set isWritable to writable of currentCalendar as string
            set isSubscribed to subscribed of currentCalendar as string
            if (count of calendarList) = 0 then
                set end of calendarList to (calendarName & "|" & isWritable & "|" & isSubscribed)
            else
                set end of calendarList to "," & (calendarName & "|" & isWritable & "|" & isSubscribed)
            end if
        end repeat
    end tell

    return calendarList as string
    """,
    result_parser=lambda x: [dict(zip(["name", "writable", "subscribed"], item.split("|"))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {},
            "output": {
                "calendars": [
                    {"name": "Home", "writable": "true", "subscribed": "true"}
                ]
            }
        }
    ]
)

# Get events
calendar_get_events = Satellite(
    name="calendar_get_events",
    description="Get events for a date range",
    category="calendar",
    parameters=[
        SatelliteParameter(
            name="start_date",
            type="string",
            description="Start date (YYYY-MM-DD)",
            required=True
        ),
        SatelliteParameter(
            name="end_date",
            type="string",
            description="End date (YYYY-MM-DD, default: start_date + 7 days)",
            required=False
        ),
        SatelliteParameter(
            name="calendar",
            type="string",
            description="Calendar name (default: all calendars)",
            required=False
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    set startDate to date "{{ start_date }}"
    {% if end_date %}
    set endDate to date "{{ end_date }}"
    {% else %}
    set endDate to startDate + (7 * days)
    {% endif %}

    tell application "Calendar"
        set eventList to {}

        {% if calendar %}
        set targetCalendar to first calendar whose name is "{{ calendar }}"
        set allEvents to every event of targetCalendar where its start date is greater than or equal to startDate and its start date is less than or equal to endDate
        {% else %}
        set allEvents to every event where its start date is greater than or equal to startDate and its start date is less than or equal to endDate
        {% endif %}

        repeat with currentEvent in allEvents
            set eventName to summary of currentEvent
            set eventStart to start date of currentEvent
            set eventEnd to end date of currentEvent
            set eventLocation to location of currentEvent
            set eventStatus to status of currentEvent
            set eventCalendar to name of calendar of currentEvent

            set eventLocation to eventLocation & ""
            set eventStatus to eventStatus & ""

            if (count of eventList) = 0 then
                set end of eventList to (eventName & "|" & (eventStart as string) & "|" & (eventEnd as string) & "|" & eventLocation & "|" & eventStatus & "|" & eventCalendar)
            else
                set end of eventList to "," & (eventName & "|" & (eventStart as string) & "|" & (eventEnd as string) & "|" & eventLocation & "|" & eventStatus & "|" & eventCalendar)
            end if
        end repeat
    end tell

    return eventList as string
    """,
    result_parser=lambda x: [dict(zip(["summary", "start", "end", "location", "status", "calendar"], item.split("|", 5))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {"start_date": "2026-01-27"},
            "output": {
                "events": [
                    {
                        "summary": "Team Meeting",
                        "start": "Monday, January 27, 2026 at 3:00:00 PM",
                        "end": "Monday, January 27, 2026 at 4:00:00 PM",
                        "location": "Conference Room",
                        "status": "",
                        "calendar": "Work"
                    }
                ]
            }
        }
    ]
)

# Create event
calendar_create_event = Satellite(
    name="calendar_create_event",
    description="Create a new calendar event",
    category="calendar",
    parameters=[
        SatelliteParameter(
            name="summary",
            type="string",
            description="Event title",
            required=True
        ),
        SatelliteParameter(
            name="start_date",
            type="string",
            description="Start date and time (YYYY-MM-DD HH:MM)",
            required=True
        ),
        SatelliteParameter(
            name="end_date",
            type="string",
            description="End date and time (YYYY-MM-DD HH:MM)",
            required=True
        ),
        SatelliteParameter(
            name="location",
            type="string",
            description="Event location",
            required=False
        ),
        SatelliteParameter(
            name="description",
            type="string",
            description="Event description",
            required=False
        ),
        SatelliteParameter(
            name="calendar",
            type="string",
            description="Calendar name (default: first calendar)",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Calendar"
        {% if calendar %}
        set targetCalendar to first calendar whose name is "{{ calendar }}"
        {% else %}
        set targetCalendar to first calendar
        {% endif %}

        tell targetCalendar
            make new event with properties {summary:"{{ summary }}", start date:date "{{ start_date }}", end date:date "{{ end_date }}"}
            {% if location %}
            set location of result to "{{ location }}"
            {% endif %}
            {% if description %}
            set description of result to "{{ description }}"
            {% endif %}
        end tell

        return "success"
    end tell
    """,
    examples=[
        {
            "input": {
                "summary": "Team Meeting",
                "start_date": "2026-01-28 15:00",
                "end_date": "2026-01-28 16:00",
                "location": "Conference Room"
            },
            "output": "success"
        }
    ]
)

# Delete event
calendar_delete_event = Satellite(
    name="calendar_delete_event",
    description="Delete a calendar event",
    category="calendar",
    parameters=[
        SatelliteParameter(
            name="summary",
            type="string",
            description="Event title",
            required=True
        ),
        SatelliteParameter(
            name="start_date",
            type="string",
            description="Event start date and time (YYYY-MM-DD HH:MM)",
            required=True
        )
    ],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Calendar"
        set targetEvent to first event where its summary is "{{ summary }}" and its start date is date "{{ start_date }}"

        if targetEvent exists then
            delete targetEvent
            return "success"
        else
            return "Error: Event not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"summary": "Old Meeting", "start_date": "2026-01-28 15:00"},
            "output": "success"
        }
    ]
)

# Export all calendar satellites
__all__ = [
    "calendar_list_calendars",
    "calendar_get_events",
    "calendar_create_event",
    "calendar_delete_event",
]
