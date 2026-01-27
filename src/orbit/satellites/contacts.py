"""Contacts station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser
import json


# Search contacts
contacts_search = Satellite(
    name="contacts_search",
    description="Search contacts by name",
    category="contacts",
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
    tell application "Contacts"
        set results to {}
        set allPeople to every person

        repeat with currentPerson in allPeople
            set personName to name of currentPerson
            if personName contains "{{ query }}" then
                set personEmail to value of email of currentPerson
                set personPhone1 to value of phone 1 of currentPerson
                set personPhone2 to value of phone 2 of currentPerson
                set personCompany to organization of currentPerson

                set personEmail to personEmail & ""
                set personPhone1 to personPhone1 & ""
                set personPhone2 to personPhone2 & ""
                set personCompany to personCompany & ""

                set end of results to (personName & "|" & personEmail & "|" & personPhone1 & "|" & personPhone2 & "|" & personCompany)
            end if
        end repeat
    end tell

    return my list(results)
    """,
    result_parser=lambda x: [dict(zip(["name", "email", "phone1", "phone2", "company"], item.split("|", 4))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {"query": "John"},
            "output": {
                "contacts": [
                    {"name": "John Doe", "email": "john@example.com", "phone1": "555-1234", "phone2": "", "company": "Acme Inc"}
                ]
            }
        }
    ]
)

# Get contact
contacts_get = Satellite(
    name="contacts_get",
    description="Get contact details by name",
    category="contacts",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Contact name",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Contacts"
        set targetPerson to first person whose name is "{{ name }}"

        if targetPerson exists then
            set personName to name of targetPerson
            set personEmail to value of email of targetPerson
            set personPhone1 to value of phone 1 of targetPerson
            set personPhone2 to value of phone 2 of targetPerson
            set personCompany to organization of targetPerson
            set personAddress to postal address of targetPerson
            set personBirthday to birthday of targetPerson
            set personNote = note of targetPerson

            set personEmail to personEmail & ""
            set personPhone1 to personPhone1 & ""
            set personPhone2 to personPhone2 & ""
            set personCompany to personCompany & ""
            set personAddress to personAddress & ""
            set personBirthday to personBirthday as string & ""
            set personNote to personNote & ""

            return personName & "|" & personEmail & "|" & personPhone1 & "|" & personPhone2 & "|" & personCompany & "|" & personAddress & "|" & personBirthday & "|" & personNote
        else
            return "Error: Contact not found"
        end if
    end tell
    """,
    result_parser=lambda x: dict(zip(["name", "email", "phone1", "phone2", "company", "address", "birthday", "note"], x.split("|", 7))) if "Error:" not in x else {"error": x},
    examples=[
        {
            "input": {"name": "John Doe"},
            "output": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone1": "555-1234",
                "phone2": "555-5678",
                "company": "Acme Inc",
                "address": "123 Main St",
                "birthday": "Monday, January 1, 1990",
                "note": "Work contact"
            }
        }
    ]
)

# Create contact
contacts_create = Satellite(
    name="contacts_create",
    description="Create new contact",
    category="contacts",
    parameters=[
        SatelliteParameter(
            name="name",
            type="string",
            description="Contact name",
            required=True
        ),
        SatelliteParameter(
            name="email",
            type="string",
            description="Email address",
            required=False
        ),
        SatelliteParameter(
            name="phone",
            type="string",
            description="Phone number",
            required=False
        ),
        SatelliteParameter(
            name="company",
            type="string",
            description="Company/organization",
            required=False
        ),
        SatelliteParameter(
            name="notes",
            type="string",
            description="Notes field",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Contacts"
        set newPerson to make new person at end of people with properties {name:"{{ name }}"}
        {% if email %}
        set email of newPerson to "{{ email }}"
        {% endif %}
        {% if phone %}
        set phone 1 of newPerson to "{{ phone }}"
        {% endif %}
        {% if company %}
        set organization of newPerson to "{{ company }}"
        {% endif %}
        {% if notes %}
        set note of newPerson to "{{ notes }}"
        {% endif %}
    end tell

    return "success"
    """,
    examples=[
        {
            "input": {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "555-9876",
                "company": "Acme Inc"
            },
            "output": "success"
        }
    ]
)

# List all contacts
contacts_list_all = Satellite(
    name="contacts_list_all",
    description="List all contacts",
    category="contacts",
    parameters=[
        SatelliteParameter(
            name="limit",
            type="integer",
            description="Maximum number of contacts",
            required=False,
            default=50
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Contacts"
        set contactList to {}
        set limitCount to {{ limit }}

        set allContacts to every person
        repeat with i from 1 to limitCount
            if i > count of allContacts then
                exit repeat
            end if

            set personName to name of currentPerson
            set end of contactList to personName
        end repeat
    end tell

    return my list(contactList)
    """,
    result_parser=lambda x: x.split(",") if x and x != "my list()" else [],
    examples=[
        {
            "input": {"limit": 10},
            "output": {"contacts": ["Alice", "Bob", "Charlie"]}
        }
    ]
)

# Export all contacts satellites
__all__ = [
    "contacts_search",
    "contacts_get",
    "contacts_create",
    "contacts_list_all",
]
