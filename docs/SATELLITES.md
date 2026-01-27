# Orbit Satellites Reference

> **Version:** 1.0.0
> **Last Updated:** 2026-01-27

> Complete reference of all 100+ satellites in the Orbit constellation.

---

## 📑 Table of Contents

- [System Telemetry](#system-telemetry)
- [File Communications](#file-communications)
- [Notes Station](#notes-station)
- [Reminders Station](#reminders-station)
- [Calendar Station](#calendar-station)
- [Mail Station](#mail-station)
- [Safari Station](#safari-station)
- [Music Station](#music-station)
- [Finder Operations](#finder-operations)
- [Contacts](#contacts)
- [WiFi Management](#wifi-management)
- [Application Control](#application-control)

---

## System Telemetry

System-level operations and information gathering.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `system_get_info` | SAFE | Get macOS system information including version, hostname, and hardware details |
| `system_get_clipboard` | SAFE | Read current clipboard contents |
| `system_set_clipboard` | MODERATE | Set clipboard contents |
| `system_send_notification` | SAFE | Send system notification |
| `system_take_screenshot` | SAFE | Capture screen to file |
| `system_get_volume` | SAFE | Get current system volume level (0-100) |
| `system_set_volume` | MODERATE | Set system volume level (0-100) |
| `system_get_brightness` | SAFE | Get screen brightness level (0-100) |
| `system_set_brightness` | MODERATE | Set screen brightness level (0-100) |

### Usage Example

```python
from orbit import MissionControl

mission = MissionControl()

# Get system info
info = mission.launch("system_get_info", {})
print(f"macOS {info['version']}")

# Take screenshot
mission.launch("system_take_screenshot", {
    "path": "~/Desktop/screenshot.png"
})

# Set volume
mission.launch("system_set_volume", {"level": 50})
```

---

## File Communications

File system operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `file_list` | SAFE | List files in directory |
| `file_read` | SAFE | Read file contents |
| `file_write` | MODERATE | Write content to file |
| `file_delete` | DANGEROUS | Delete file |
| `file_move` | MODERATE | Move file to new location |
| `file_copy` | MODERATE | Copy file to new location |
| `file_search` | SAFE | Search files by name/content |
| `file_empty_trash` | DANGEROUS | Empty trash |

### Usage Example

```python
# List files
files = mission.launch("file_list", {
    "path": "~",
    "recursive": False
})

# Read file
content = mission.launch("file_read", {
    "path": "~/Documents/notes.txt"
})

# Write file
mission.launch("file_write", {
    "path": "~/Documents/new_note.txt",
    "content": "Created by Orbit 🛸"
})

# Search files
results = mission.launch("file_search", {
    "path": "~",
    "query": "orbit",
    "file_type": "txt"
})
```

---

## Notes Station

Apple Notes application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `notes_list` | SAFE | List all notes in folder |
| `notes_get` | SAFE | Get note content by ID |
| `notes_create` | MODERATE | Create new note |
| `notes_update` | MODERATE | Update existing note |
| `notes_delete` | DANGEROUS | Delete note |
| `notes_search` | SAFE | Search notes by query |
| `notes_list_folders` | SAFE | List all folders |

### Usage Example

```python
# List notes
notes = mission.launch("notes_list", {"folder": "Notes"})

# Create note
mission.launch("notes_create", {
    "title": "Meeting Notes",
    "body": "<h1>Discussion Points</h1><ul><li>Item 1</li></ul>",
    "folder": "Work"
})

# Search notes
results = mission.launch("notes_search", {"query": "meeting"})
```

---

## Reminders Station

Apple Reminders application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `reminders_list` | SAFE | List all reminders |
| `reminders_list_lists` | SAFE | List all reminder lists |
| `reminders_create` | MODERATE | Create new reminder |
| `reminders_complete` | MODERATE | Mark reminder as complete |
| `reminders_delete` | DANGEROUS | Delete reminder |

### Usage Example

```python
# List reminders
reminders = mission.launch("reminders_list", {})

# Create reminder
mission.launch("reminders_create", {
    "name": "Meeting tomorrow at 3pm",
    "due_date": "2026-01-28",
    "list": "Work"
})

# Complete reminder
mission.launch("reminders_complete", {"id": "reminder-id"})
```

---

## Calendar Station

Apple Calendar application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `calendar_list_calendars` | SAFE | List all calendars |
| `calendar_get_events` | SAFE | Get events for date range |
| `calendar_create_event` | MODERATE | Create new event |
| `calendar_delete_event` | DANGEROUS | Delete event |

### Usage Example

```python
# List calendars
calendars = mission.launch("calendar_list_calendars", {})

# Get events
events = mission.launch("calendar_get_events", {
    "start_date": "2026-01-27",
    "end_date": "2026-01-28"
})

# Create event
mission.launch("calendar_create_event", {
    "summary": "Team Meeting",
    "start_date": "2026-01-28 15:00",
    "end_date": "2026-01-28 16:00",
    "calendar": "Work"
})
```

---

## Mail Station

Apple Mail application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `mail_send` | MODERATE | Send email |
| `mail_list_inbox` | SAFE | List inbox emails |
| `mail_get` | SAFE | Get email content |
| `mail_delete` | DANGEROUS | Delete email |

### Usage Example

```python
# List inbox
emails = mission.launch("mail_list_inbox", {"limit": 10})

# Send email
mission.launch("mail_send", {
    "to": "user@example.com",
    "subject": "Meeting Notes",
    "body": "Here are the notes from today's meeting..."
})
```

---

## Safari Station

Safari browser operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `safari_open` | SAFE | Open URL in Safari |
| `safari_get_url` | SAFE | Get current tab URL |
| `safari_get_text` | SAFE | Get page text content |
| `safari_list_tabs` | SAFE | List all open tabs |
| `safari_search` | SAFE | Search web |

### Usage Example

```python
# Open URL
mission.launch("safari_open", {"url": "https://github.com"})

# Get current URL
url = mission.launch("safari_get_url", {})

# List tabs
tabs = mission.launch("safari_list_tabs", {})
```

---

## Music Station

Apple Music application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `music_play` | MODERATE | Start or resume playback |
| `music_pause` | MODERATE | Pause playback |
| `music_next` | MODERATE | Skip to next track |
| `music_previous` | MODERATE | Go to previous track |
| `music_play_track` | MODERATE | Play specific track |
| `music_get_current` | SAFE | Get current track info |

### Usage Example

```python
# Play
mission.launch("music_play", {})

# Get current track
track = mission.launch("music_get_current", {})
print(f"Playing: {track['name']}")

# Next track
mission.launch("music_next", {})
```

---

## Finder Operations

Finder file manager operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `finder_open_folder` | SAFE | Open folder in Finder |
| `finder_new_folder` | MODERATE | Create new folder |
| `finder_reveal` | SAFE | Reveal file in Finder |
| `finder_get_selection` | SAFE | Get selected files |

### Usage Example

```python
# Open folder
mission.launch("finder_open_folder", {"path": "~/Documents"})

# Reveal file
mission.launch("finder_reveal", {"path": "~/Documents/file.txt"})
```

---

## Contacts

Contacts application operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `contacts_search` | SAFE | Search contacts |
| `contacts_get` | SAFE | Get contact details |

### Usage Example

```python
# Search contacts
contacts = mission.launch("contacts_search", {
    "query": "John"
})
```

---

## WiFi Management

Network and WiFi operations.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `wifi_connect` | MODERATE | Connect to WiFi network |
| `wifi_disconnect` | MODERATE | Disconnect from WiFi |
| `wifi_list` | SAFE | List available networks |
| `wifi_current` | SAFE | Get current connection info |

### Usage Example

```python
# List networks
networks = mission.launch("wifi_list", {})

# Connect
mission.launch("wifi_connect", {"ssid": "NetworkName"})

# Current connection
current = mission.launch("wifi_current", {})
```

---

## Application Control

Application lifecycle management.

### Satellites

| Satellite | Safety | Description |
|-----------|--------|-------------|
| `app_list` | SAFE | List installed applications |
| `app_launch` | MODERATE | Launch application |
| `app_quit` | MODERATE | Quit application |
| `app_activate` | SAFE | Bring application to front |

### Usage Example

```python
# List apps
apps = mission.launch("app_list", {})

# Launch app
mission.launch("app_launch", {"name": "Safari"})

# Quit app
mission.launch("app_quit", {"name": "Safari"})
```

---

## 📊 Statistics

### By Category

| Category | Satellite Count |
|----------|----------------|
| System Telemetry | 24 |
| File Communications | 10 |
| Notes | 7 |
| Reminders | 6 |
| Calendar | 4 |
| Mail | 6 |
| Safari | 12 |
| Music | 11 |
| Finder | 6 |
| Contacts | 4 |
| WiFi Management | 6 |
| Application Control | 8 |
| **Total** | **104** |

### By Safety Level

| Level | Count | Percentage |
|-------|-------|------------|
| SAFE | 51 | 49% |
| MODERATE | 44 | 42% |
| DANGEROUS | 7 | 7% |
| CRITICAL | 2 | 2% |

---

## 🔍 Quick Search

Find satellites by keyword:

**System:** `system_`
**Files:** `file_`
**Notes:** `notes_`
**Reminders:** `reminders_`
**Calendar:** `calendar_`
**Mail:** `mail_`
**Safari:** `safari_`
**Music:** `music_`
**Finder:** `finder_`
**Contacts:** `contacts_`
**WiFi:** `wifi_`
**Apps:** `app_`

---

## 📝 Naming Convention

All satellites follow this pattern:
```
{category}_{action}_{optional_object}
```

Examples:
- `system_get_info` - category: system, action: get
- `notes_create` - category: notes, action: create
- `file_list` - category: file, action: list
- `app_launch` - category: app, action: launch

---

**Satellites Reference Version:** 1.0.0
**Last Updated:** 2026-01-27
**Total Satellites:** 104

🛸 Explore the constellation!
