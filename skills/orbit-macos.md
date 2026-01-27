# orbit-macos

**Teach Claude how to use Orbit - A macOS automation toolkit with 104+ satellites**

## Installation

```bash
pip install orbit-macos
```

Verify installation:
```bash
python -c "from orbit import MissionControl; print('✅ Orbit installed')"
orbit --version
```

## Core Concepts

**Orbit Architecture:**
- **MissionControl**: Central command hub
- **Satellites**: 104 individual automation tools
- **Constellation**: Collection of registered satellites
- **4 Safety Levels**: SAFE, MODERATE, DANGEROUS, CRITICAL

## Basic Usage

### Python SDK

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

# Initialize
mission = MissionControl()
mission.register_constellation(all_satellites)

# Execute
result = mission.launch("system_get_info", {})
print(result)
```

### CLI

```bash
# List satellites
orbit list

# Search
orbit search "safari"

# Execute
orbit run system_get_info

# Interactive mode
orbit repl
```

## Satellite Categories (104 total)

### System (24 satellites)
**Basic:**
- `system_get_info` [SAFE] - System information
- `system_get_clipboard` [SAFE] - Read clipboard
- `system_set_clipboard` [MODERATE] - Set clipboard
- `system_send_notification` [SAFE] - Send notification
- `system_take_screenshot` [SAFE] - Capture screen
- `system_get/set_volume` [SAFE/MODERATE] - Volume control
- `system_get/set_brightness` [SAFE/MODERATE] - Brightness control

**Enhanced:**
- `system_get_detailed_info` [SAFE] - Detailed system info
- `system_get_clipboard_history` [SAFE] - Clipboard history
- `system_clear_clipboard` [MODERATE] - Clear clipboard
- `system_take_screenshot_selection/window` [SAFE] - Selective screenshots
- `system_mute/unmute_volume` [MODERATE] - Mute controls
- `system_volume_up/down` [MODERATE] - Volume adjustments
- `system_brightness_up/down` [MODERATE] - Brightness adjustments
- `system_sleep` [MODERATE] - Sleep system
- `system_reboot` [DANGEROUS] - Reboot
- `system_shutdown` [CRITICAL] - Shutdown

### Files (11 satellites)
- `file_list` [SAFE] - List files
- `file_read` [SAFE] - Read file
- `file_write` [MODERATE] - Write file
- `file_delete` [DANGEROUS] - Delete file
- `file_move` [MODERATE] - Move file
- `file_copy` [MODERATE] - Copy file
- `file_search` [SAFE] - Search files
- `file_empty_trash` [DANGEROUS] - Empty trash
- `file_create_directory` [MODERATE] - Create directory
- `file_get_info` [SAFE] - File metadata

### Notes (7 satellites)
- `notes_list` [SAFE] - List notes
- `notes_get` [SAFE] - Get note
- `notes_create` [MODERATE] - Create note
- `notes_update` [MODERATE] - Update note
- `notes_delete` [DANGEROUS] - Delete note
- `notes_search` [SAFE] - Search notes
- `notes_list_folders` [SAFE] - List folders

### Reminders (6 satellites)
- `reminders_list` [SAFE] - List reminders
- `reminders_create` [MODERATE] - Create reminder
- `reminders_complete` [MODERATE] - Complete reminder
- `reminders_uncomplete` [MODERATE] - Uncomplete reminder
- `reminders_delete` [DANGEROUS] - Delete reminder
- `reminders_list_lists` [SAFE] - List lists

### Calendar (4 satellites)
- `calendar_list_calendars` [SAFE] - List calendars
- `calendar_get_events` [SAFE] - Get events
- `calendar_create_event` [MODERATE] - Create event
- `calendar_delete_event` [DANGEROUS] - Delete event

### Mail (6 satellites)
- `mail_send` [MODERATE] - Send email
- `mail_list_inbox` [SAFE] - List emails
- `mail_get` [SAFE] - Get email
- `mail_delete` [DANGEROUS] - Delete email
- `mail_mark_as_read` [MODERATE] - Mark read
- `mail_mark_as_unread` [MODERATE] - Mark unread

### Safari (11 satellites)
- `safari_open` [SAFE] - Open URL
- `safari_get_url` [SAFE] - Get current URL
- `safari_get_text` [SAFE] - Get page text
- `safari_list_tabs` [SAFE] - List tabs
- `safari_close_tab` [SAFE] - Close tab
- `safari_search` [SAFE] - Search web
- `safari_new_tab` [SAFE] - New tab
- `safari_go_back/forward` [SAFE] - Navigation
- `safari_refresh` [SAFE] - Refresh page
- `safari_zoom_in/out` [SAFE] - Zoom controls

### Music (11 satellites)
- `music_play` [MODERATE] - Play
- `music_pause` [MODERATE] - Pause
- `music_next/previous` [MODERATE] - Skip tracks
- `music_get_current` [SAFE] - Current track
- `music_set/get_volume` [MODERATE/SAFE] - Volume
- `music_play_track` [MODERATE] - Play specific track
- `music_search` [SAFE] - Search music
- `music_get_playlists` [SAFE] - Get playlists
- `music_shuffle` [MODERATE] - Toggle shuffle

### Finder (6 satellites)
- `finder_open_folder` [SAFE] - Open folder
- `finder_new_folder` [MODERATE] - Create folder
- `finder_reveal` [SAFE] - Reveal file
- `finder_get_selection` [SAFE] - Get selection
- `finder_empty_trash` [DANGEROUS] - Empty trash
- `finder_get_trash_info` [SAFE] - Trash info

### Contacts (4 satellites)
- `contacts_search` [SAFE] - Search contacts
- `contacts_get` [SAFE] - Get contact
- `contacts_create` [MODERATE] - Create contact
- `contacts_list_all` [SAFE] - List all

### WiFi (6 satellites)
- `wifi_connect` [MODERATE] - Connect to network
- `wifi_disconnect` [MODERATE] - Disconnect
- `wifi_list` [SAFE] - List networks
- `wifi_current` [SAFE] - Current connection
- `wifi_turn_on/off` [MODERATE] - Toggle WiFi

### Applications (8 satellites)
- `app_list` [SAFE] - List apps
- `app_launch` [MODERATE] - Launch app
- `app_quit` [MODERATE] - Quit app
- `app_activate` [SAFE] - Activate app
- `app_get_running` [SAFE] - Running apps
- `app_force_quit` [DANGEROUS] - Force quit
- `app_hide` [MODERATE] - Hide app
- `app_show` [MODERATE] - Show app

## Common Tasks

### Get System Information
```python
result = mission.launch("system_get_info", {})
# Returns: version, hostname, username, architecture
```

### Read/Write Files
```python
# Read
content = mission.launch("file_read", {"path": "~/Documents/notes.txt"})

# Write
mission.launch("file_write", {
    "path": "~/Documents/new_note.txt",
    "content": "Hello from Orbit"
})
```

### Create Note
```python
mission.launch("notes_create", {
    "title": "Meeting Notes",
    "body": "<h1>Discussion</h1><ul><li>Item 1</li></ul>",
    "folder": "Work"
})
```

### Send Email
```python
mission.launch("mail_send", {
    "to": "user@example.com",
    "subject": "Meeting Notes",
    "body": "Here are the notes..."
})
```

### Control Music
```python
# Get current track
track = mission.launch("music_get_current", {})

# Play next
mission.launch("music_next", {})

# Search and play
results = mission.launch("music_search", {"query": "jazz"})
```

### Safari Automation
```python
# Open URL
mission.launch("safari_open", {"url": "https://github.com"})

# Get current page URL
url = mission.launch("safari_get_url", {})

# List all tabs
tabs = mission.launch("safari_list_tabs", {})
```

## Safety System

**Safety Levels:**
- **SAFE** (49%) - Read-only, no prompts
- **MODERATE** (42%) - Non-destructive, prompt recommended
- **DANGEROUS** (7%) - Destructive, explicit approval required
- **CRITICAL** (2%) - System-level, maximum caution

**Custom Safety Rules:**
```python
from orbit import SafetyShield, SafetyLevel

# Conservative shield
shield = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "prompt",
    SafetyLevel.DANGEROUS: "deny",
    SafetyLevel.CRITICAL: "deny"
})

mission = MissionControl(safety_shield=shield)
```

## AI Framework Integration

### OpenAI Functions
```python
import openai
from orbit import MissionControl

mission = MissionControl()
mission.register_constellation(all_satellites)

# Export functions
functions = mission.export_to_openai_functions()

# Use with OpenAI
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Take a screenshot"}],
    functions=functions
)
```

### LangChain
```python
from langchain.tools import Tool

tools = [
    Tool(
        name=sat.name,
        func=lambda kwargs, sat=sat: mission.launch(sat.name, kwargs),
        description=sat.description
    )
    for sat in mission.constellation.list_all()
]
```

## CLI Commands

```bash
# List satellites by category
orbit list -c system
orbit list -c music -s safe

# Search
orbit search "screenshot"

# Execute with parameters
orbit run system_set_volume --level 50

# Export to formats
orbit export openai-functions > orbit_functions.json
orbit export json-schema > orbit_schema.json
```

## Troubleshooting

**"AppleScript execution failed"**
- Grant Accessibility permissions: System Settings → Privacy & Security → Accessibility
- Enable Automation permissions for Terminal/IDE

**"Satellite not found"**
- Register satellite first: `mission.register(satellite)`
- Check registered satellites: `mission.constellation.list_all()`

**"Permission denied"**
- Use absolute paths
- Check file permissions: `ls -la ~/path/to/file`

**"Module not found"**
- Reinstall: `pip uninstall orbit-macos && pip install orbit-macos`

## Best Practices

1. **Always check results**
```python
result = mission.launch("file_write", {...})
if result.get("success"):
    print("Success")
```

2. **Handle errors gracefully**
```python
try:
    result = mission.launch("file_delete", {...})
except Exception as e:
    print(f"Error: {e}")
```

3. **Register only what you need**
```python
from orbit.satellites import system_satellites
mission.register_constellation(system_satellites)
```

4. **Use absolute paths**
```python
import os
path = os.path.expanduser("~/Documents/file.txt")
mission.launch("file_read", {"path": path})
```

## Quick Reference

**Naming Convention:** `{category}_{action}_{optional_object}`

**Examples:**
- `system_get_info` - category: system, action: get
- `notes_create` - category: notes, action: create
- `file_list` - category: file, action: list
- `app_launch` - category: app, action: launch

## Resources

- GitHub: https://github.com/xiaoxiath/orbit
- PyPI: https://pypi.org/project/orbit-macos/
- Docs: https://github.com/xiaoxiath/orbit/tree/main/docs
- Version: 1.0.0
- Total Satellites: 104
- Categories: 12
