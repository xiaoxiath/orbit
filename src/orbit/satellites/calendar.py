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
            set isWritable to writable of currentCalendar
            try
                set isSubscribed to subscribed of currentCalendar
            on error
                set isSubscribed to missing value
            end try

            if isSubscribed is missing value then
                set isSubscribed to "false"
            else
                set isSubscribed to isSubscribed as string
            end if

            if (count of calendarList) = 0 then
                set end of calendarList to (calendarName & "|" & (isWritable as string) & "|" & isSubscribed)
            else
                set end of calendarList to "," & (calendarName & "|" & (isWritable as string) & "|" & isSubscribed)
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
    -- Parse date string in a locale-independent way
    set startDate to parseISODate("{{ start_date }}")

    {% if end_date %}
    set endDate to parseISODate("{{ end_date }}")
    {% else %}
    set endDate to startDate + (7 * days)
    {% endif %}

    tell application "Calendar"
        set eventList to {}

        {% if calendar %}
        set targetCalendar to first calendar whose name is "{{ calendar }}"
        set allCalendars to {targetCalendar}
        {% else %}
        set allCalendars to every calendar
        {% endif %}

        repeat with currentCalendar in allCalendars
            set allEvents to every event of currentCalendar

            repeat with currentEvent in allEvents
                set eventStart to start date of currentEvent

                -- Manual date comparison (more reliable)
                if (eventStart is greater than or equal to startDate) and (eventStart is less than or equal to endDate) then
                    set eventName to summary of currentEvent
                    set eventEnd to end date of currentEvent
                    set eventLocation to location of currentEvent
                    set eventStatus to status of currentEvent

                    -- Get calendar name with error handling
                    try
                        set eventCalendar to name of calendar of currentEvent
                    on error
                        set eventCalendar to name of currentCalendar
                    end try

                    set eventLocation to eventLocation & ""
                    set eventStatus to eventStatus & ""

                    if (count of eventList) = 0 then
                        set end of eventList to (eventName & "|" & (eventStart as string) & "|" & (eventEnd as string) & "|" & eventLocation & "|" & eventStatus & "|" & eventCalendar)
                    else
                        set end of eventList to "," & (eventName & "|" & (eventStart as string) & "|" & (eventEnd as string) & "|" & eventLocation & "|" & eventStatus & "|" & eventCalendar)
                    end if
                end if
            end repeat
        end repeat
    end tell

    return eventList as string

    on parseISODate(isoDate)
        -- Parse YYYY-MM-DD format and create a date object
        -- This method uses current date and modifies it, which is more reliable
        set savedDelimiters to AppleScript's text item delimiters
        set AppleScript's text item delimiters to "-"
        set dateParts to text items of isoDate
        set AppleScript's text item delimiters to savedDelimiters

        set y to item 1 of dateParts as integer
        set m to item 2 of dateParts as integer
        set d to item 3 of dateParts as integer

        set newDate to current date
        set newDate's year to y
        set newDate's month to m
        set newDate's day to d
        set newDate's time to 0

        return newDate
    end parseISODate
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
    -- Parse date strings in a locale-independent way
    set startDate to parseDateTime("{{ start_date }}")
    set endDate to parseDateTime("{{ end_date }}")

    tell application "Calendar"
        {% if calendar %}
        set targetCalendar to first calendar whose name is "{{ calendar }}"
        {% else %}
        set targetCalendar to first calendar
        {% endif %}

        tell targetCalendar
            set newEvent to make new event with properties {summary:"{{ summary }}", start date:startDate, end date:endDate}
            {% if location %}
            set location of newEvent to "{{ location }}"
            {% endif %}
            {% if description %}
            set description of newEvent to "{{ description }}"
            {% endif %}
        end tell

        return "success"
    end tell

    on parseDateTime(dateTimeStr)
        -- Parse YYYY-MM-DD HH:MM format and create a date object
        set savedDelimiters to AppleScript's text item delimiters
        set AppleScript's text item delimiters to " "
        set dateTimeParts to text items of dateTimeStr
        set AppleScript's text item delimiters to savedDelimiters

        set datePart to item 1 of dateTimeParts
        set timePart to item 2 of dateTimeParts

        -- Parse date
        set AppleScript's text item delimiters to "-"
        set dateParts to text items of datePart
        set AppleScript's text item delimiters to savedDelimiters

        set y to item 1 of dateParts as integer
        set m to item 2 of dateParts as integer
        set d to item 3 of dateParts as integer

        -- Parse time
        set AppleScript's text item delimiters to ":"
        set timeParts to text items of timePart
        set AppleScript's text item delimiters to savedDelimiters

        set hr to item 1 of timeParts as integer
        set mn to item 2 of timeParts as integer

        set newDate to current date
        set newDate's year to y
        set newDate's month to m
        set newDate's day to d
        set newDate's hours to hr
        set newDate's minutes to mn
        set newDate's seconds to 0

        return newDate
    end parseDateTime
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
    -- Parse date string in a locale-independent way
    set startDate to parseDateTime("{{ start_date }}")

    tell application "Calendar"
        set targetEvent to missing value
        set allCalendars to every calendar

        repeat with currentCalendar in allCalendars
            set allEvents to every event of currentCalendar

            repeat with currentEvent in allEvents
                set eventName to summary of currentEvent
                set eventStart to start date of currentEvent

                -- Compare event name and start date (within 1 minute tolerance)
                if eventName is "{{ summary }}" then
                    set timeDiff to (eventStart - startDate)
                    if (timeDiff > -60) and (timeDiff < 60) then
                        set targetEvent to currentEvent
                        exit repeat
                    end if
                end if
            end repeat

            if targetEvent is not missing value then
                exit repeat
            end if
        end repeat

        if targetEvent is not missing value then
            delete targetEvent
            return "success"
        else
            return "Error: Event not found"
        end if
    end tell

    on parseDateTime(dateTimeStr)
        -- Parse YYYY-MM-DD HH:MM format and create a date object
        set savedDelimiters to AppleScript's text item delimiters
        set AppleScript's text item delimiters to " "
        set dateTimeParts to text items of dateTimeStr
        set AppleScript's text item delimiters to savedDelimiters

        set datePart to item 1 of dateTimeParts
        set timePart to item 2 of dateTimeParts

        -- Parse date
        set AppleScript's text item delimiters to "-"
        set dateParts to text items of datePart
        set AppleScript's text item delimiters to savedDelimiters

        set y to item 1 of dateParts as integer
        set m to item 2 of dateParts as integer
        set d to item 3 of dateParts as integer

        -- Parse time
        set AppleScript's text item delimiters to ":"
        set timeParts to text items of timePart
        set AppleScript's text item delimiters to savedDelimiters

        set hr to item 1 of timeParts as integer
        set mn to item 2 of timeParts as integer

        set newDate to current date
        set newDate's year to y
        set newDate's month to m
        set newDate's day to d
        set newDate's hours to hr
        set newDate's minutes to mn
        set newDate's seconds to 0

        return newDate
    end parseDateTime
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
