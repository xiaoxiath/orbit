"""Mail station satellites."""

from orbit.core import Satellite, SatelliteParameter, SafetyLevel


# Send email
mail_send = Satellite(
    name="mail_send",
    description="Send an email",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="to",
            type="string",
            description="Recipient email address",
            required=True
        ),
        SatelliteParameter(
            name="subject",
            type="string",
            description="Email subject",
            required=True
        ),
        SatelliteParameter(
            name="body",
            type="string",
            description="Email body content",
            required=True
        ),
        SatelliteParameter(
            name="cc",
            type="string",
            description="CC recipients (comma-separated)",
            required=False
        ),
        SatelliteParameter(
            name="bcc",
            type="string",
            description="BCC recipients (comma-separated)",
            required=False
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Mail"
        activate
        set newMessage to make new outgoing message with properties {subject:"{{ subject }}", content:"{{ body }}", visible:true}

        tell newMessage
            make new to recipient with "{{ to }}"
            {% if cc %}
            make new to recipient with "{{ cc }}" with copy to
            {% endif %}
            {% if bcc %}
            make new to recipient with "{{ bcc }}" with blind carbon copy
            {% endif %}
        end tell

        send newMessage
        return "success"
    end tell
    """,
    examples=[
        {
            "input": {
                "to": "user@example.com",
                "subject": "Meeting Notes",
                "body": "Here are the notes from today's meeting..."
            },
            "output": "success"
        }
    ]
)

# List inbox
mail_list_inbox = Satellite(
    name="mail_list_inbox",
    description="List emails in inbox",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="limit",
            type="integer",
            description="Maximum number of emails to return",
            required=False,
            default=10
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Mail"
        set inboxMessages to {}
        set limitCount to {{ limit }}

        set inbox to mailbox "INBOX"
        set allMessages to (messages of inbox)

        repeat with i from 1 to limitCount
            if i > count of allMessages then
                exit repeat
            end if

            set currentMessage to item i of allMessages
            set messageSubject to subject of currentMessage
            set messageSender to sender of currentMessage
            set messageDate = date received of currentMessage
            set messageRead (read status of currentMessage as string)

            set end of inboxMessages to (messageSubject & "|" & messageSender & "|" & messageDate & "|" & messageRead)
        end repeat
    end tell

    return my list(inboxMessages)
    """,
    result_parser=lambda x: [dict(zip(["subject", "sender", "date", "read"], item.split("|", 3))) for item in x.split(",")] if x else [],
    examples=[
        {
            "input": {"limit": 5},
            "output": {
                "emails": [
                    {"subject": "Meeting Update", "sender": "colleague@company.com", "date": "Monday", "read": "false"}
                ]
            }
        }
    ]
)

# Get email content
mail_get = Satellite(
    name="mail_get",
    description="Get email content by subject",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="subject",
            type="string",
            description="Email subject to retrieve",
            required=True
        )
    ],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "Mail"
        set targetMessage to first message of mailbox "INBOX" whose subject is "{{ subject }}"

        if targetMessage exists then
            set messageContent to content of targetMessage
            set messageSender to sender of targetMessage
            return messageContent & "|" & messageSender
        else
            return "Error: Message not found"
        end if
    end tell
    """,
    result_parser=lambda x: dict(zip(["content", "sender"], x.split("|", 1))) if "Error:" not in x else {"error": x},
    examples=[
        {
            "input": {"subject": "Meeting Notes"},
            "output": {"content": "Email content...", "sender": "sender@example.com"}
        }
    ]
)

# Delete email
mail_delete = Satellite(
    name="mail_delete",
    description="Delete an email",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="subject",
            type="string",
            description="Subject of email to delete",
            required=True
        )
    ],
    safety_level=SafetyLevel.DANGEROUS,
    applescript_template="""
    tell application "Mail"
        set targetMessage to first message of mailbox "INBOX" whose subject is "{{ subject }}"

        if targetMessage exists then
            delete targetMessage
            return "success"
        else
            return "Error: Message not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"subject": "Old Email"},
            "output": "success"
        }
    ]
)

# Mark as read/unread
mail_mark_as_read = Satellite(
    name="mail_mark_as_read",
    description="Mark email as read",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="subject",
            type="string",
            description="Subject of email to mark",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Mail"
        set targetMessage to first message of mailbox "INBOX" whose subject is "{{ subject }}"

        if targetMessage exists then
            set read status of targetMessage to true
            return "success"
        else
            return "Error: Message not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"subject": "Meeting Update"},
            "output": "success"
        }
    ]
)

mail_mark_as_unread = Satellite(
    name="mail_mark_as_unread",
    description="Mark email as unread",
    category="mail",
    parameters=[
        SatelliteParameter(
            name="subject",
            type="string",
            description="Subject of email to mark",
            required=True
        )
    ],
    safety_level=SafetyLevel.MODERATE,
    applescript_template="""
    tell application "Mail"
        set targetMessage to first message of mailbox "INBOX" whose subject is "{{ subject }}"

        if targetMessage exists then
            set read status of targetMessage to false
            return "success"
        else
            return "Error: Message not found"
        end if
    end tell
    """,
    examples=[
        {
            "input": {"subject": "Meeting Update"},
            "output": "success"
        }
    ]
)

# Export all mail satellites
__all__ = [
    "mail_send",
    "mail_list_inbox",
    "mail_get",
    "mail_delete",
    "mail_mark_as_read",
    "mail_mark_as_unread",
]
