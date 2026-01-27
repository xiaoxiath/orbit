# Orbit macOS Automation - Complete Skill Guide

> 🛸 **Teach Claude to master Orbit**: A framework-agnostic macOS automation toolkit with 104+ satellites

---

## 🎯 Purpose

This skill enables Claude to:
1. Install and configure Orbit on macOS systems
2. Use all 104 satellites across 12 application categories
3. Write Python automation scripts using MissionControl
4. Execute commands via CLI
5. Integrate with AI frameworks (OpenAI, LangChain, Anthropic)
6. Follow safety protocols and best practices

---

## 📋 Prerequisites Check

Before using Orbit, verify the system meets requirements:

```bash
# Check macOS version (must be 12.0+)
sw_vers

# Check Python version (must be 3.10+)
python3 --version

# Check admin access (required for some operations)
groups
```

**Required:**
- macOS 12.0+ (Monterey or later)
- Python 3.10 or higher
- Administrator access (for some AppleScript operations)

---

## 🚀 Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Install Orbit
pip install orbit-macos

# Verify installation
python -c "from orbit import MissionControl; print('✅ Orbit installed successfully!')"

# Check CLI
orbit --version
```

### Method 2: Install from Source

```bash
# Clone repository
git clone https://github.com/xiaoxiath/orbit.git
cd orbit

# Install in development mode
pip install -e .

# Or install from built package
poetry build
pip install dist/orbit_macos-1.0.0-py3-none-any.whl
```

### Method 3: Install with Poetry

```bash
# Clone repository
git clone https://github.com/xiaoxiath/orbit.git
cd orbit

# Install with Poetry
poetry install

# Verify
poetry run orbit --version
```

---

## 🧠 Quick Mental Model

**Orbit = Mission Control + Satellites**

- **MissionControl**: Central command hub that manages and executes satellites
- **Satellites**: Individual automation tools (104 total) for specific macOS apps
- **Constellation**: Collection of registered satellites
- **Launcher**: Executes satellite commands (AppleScript under the hood)
- **SafetyShield**: Security layer with 4 levels (SAFE, MODERATE, DANGEROUS, CRITICAL)

**Think of it as:**
```
You (Claude) → MissionControl → Launcher → AppleScript → macOS Apps
```

---

## 🛠️ Core Usage Patterns

### Pattern 1: Basic Python SDK Usage

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

# Initialize mission control
mission = MissionControl()

# Register all satellites
mission.register_constellation(all_satellites)

# Execute a satellite
result = mission.launch("system_get_info", {})

print(result)
# Output: {'version': '14.0', 'hostname': 'MacBook-Pro', ...}
```

### Pattern 2: Register Specific Categories

```python
from orbit import MissionControl
from orbit.satellites import (
    system_satellites,
    file_satellites,
    notes_satellites
)

mission = MissionControl()

# Register only what you need
mission.register_constellation(system_satellites)
mission.register_constellation(file_satellites)

# Now you can use these satellites
result = mission.launch("system_get_info", {})
```

### Pattern 3: CLI Usage

```bash
# List available satellites
orbit list

# Search for satellites
orbit search "safari"

# Execute a satellite
orbit run system_get_info

# Get detailed info
orbit info system_get_info

# Interactive mode
orbit repl
```

### Pattern 4: With Safety Controls

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# Create custom safety rules
shield = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "prompt",  # Ask user
    SafetyLevel.DANGEROUS: "deny",   # Block
    SafetyLevel.CRITICAL: "deny"
})

mission = MissionControl(safety_shield=shield)

# Now DANGEROUS operations will be blocked
result = mission.launch("file_delete", {"path": "~/test.txt"})
# Will be blocked due to safety rule
```

---

## 📚 Complete Satellite Reference

### 🖥️ System Satellites (24 satellites)

**Basic System (9):**
- `system_get_info` [SAFE] - Get macOS system info
- `system_get_clipboard` [SAFE] - Read clipboard
- `system_set_clipboard` [MODERATE] - Set clipboard
- `system_send_notification` [SAFE] - Send notification
- `system_take_screenshot` [SAFE] - Capture screen
- `system_get_volume` [SAFE] - Get volume (0-100)
- `system_set_volume` [MODERATE] - Set volume
- `system_get_brightness` [SAFE] - Get brightness (0-100)
- `system_set_brightness` [MODERATE] - Set brightness

**Enhanced System (15):**
- `system_get_detailed_info` [SAFE] - Detailed system info
- `system_get_clipboard_history` [SAFE] - Get clipboard history
- `system_clear_clipboard` [MODERATE] - Clear clipboard
- `system_send_notification_with_sound` [SAFE] - Notification with sound
- `system_take_screenshot_selection` [SAFE] - Screenshot selection
- `system_take_screenshot_window` [SAFE] - Screenshot window
- `system_mute_volume` [MODERATE] - Mute volume
- `system_unmute_volume` [MODERATE] - Unmute volume
- `system_volume_up` [MODERATE] - Volume up
- `system_volume_down` [MODERATE] - Volume down
- `system_brightness_up` [MODERATE] - Brightness up
- `system_brightness_down` [MODERATE] - Brightness down
- `system_sleep` [MODERATE] - Sleep system
- `system_reboot` [DANGEROUS] - Reboot system
- `system_shutdown` [CRITICAL] - Shutdown system

**Usage Examples:**
```python
# Get system info
info = mission.launch("system_get_info", {})

# Take screenshot
mission.launch("system_take_screenshot", {"path": "~/Desktop/screenshot.png"})

# Set volume to 50%
mission.launch("system_set_volume", {"level": 50})

# Send notification
mission.launch("system_send_notification", {
    "title": "Hello",
    "message": "Orbit is running!"
})
```

---

### 📁 File Satellites (11 satellites)

- `file_list` [SAFE] - List files in directory
- `file_read` [SAFE] - Read file content
- `file_write` [MODERATE] - Write to file
- `file_delete` [DANGEROUS] - Delete file
- `file_move` [MODERATE] - Move file
- `file_copy` [MODERATE] - Copy file
- `file_search` [SAFE] - Search files
- `file_empty_trash` [DANGEROUS] - Empty trash
- `file_create_directory` [MODERATE] - Create directory
- `file_get_info` [SAFE] - Get file metadata

**Usage Examples:**
```python
# List files in Documents
files = mission.launch("file_list", {
    "path": "~/Documents",
    "recursive": False
})

# Read a file
content = mission.launch("file_read", {
    "path": "~/Documents/notes.txt"
})

# Write a file
mission.launch("file_write", {
    "path": "~/Documents/new_note.txt",
    "content": "Created by Orbit"
})

# Search for Python files
results = mission.launch("file_search", {
    "path": "~",
    "query": "test",
    "file_type": "py"
})
```

---

### 📝 Notes Satellites (7 satellites)

- `notes_list` [SAFE] - List notes in folder
- `notes_get` [SAFE] - Get note by ID
- `notes_create` [MODERATE] - Create new note
- `notes_update` [MODERATE] - Update existing note
- `notes_delete` [DANGEROUS] - Delete note
- `notes_search` [SAFE] - Search notes
- `notes_list_folders` [SAFE] - List all folders

**Usage Examples:**
```python
# List all notes
notes = mission.launch("notes_list", {"folder": "Notes"})

# Create a note
mission.launch("notes_create", {
    "title": "Meeting Notes",
    "body": "<h1>Discussion Points</h1><ul><li>Item 1</li></ul>",
    "folder": "Work"
})

# Search notes
results = mission.launch("notes_search", {"query": "meeting"})
```

---

### ✅ Reminders Satellites (6 satellites)

- `reminders_list` [SAFE] - List all reminders
- `reminders_create` [MODERATE] - Create reminder
- `reminders_complete` [MODERATE] - Mark as complete
- `reminders_uncomplete` [MODERATE] - Mark as incomplete
- `reminders_delete` [DANGEROUS] - Delete reminder
- `reminders_list_lists` [SAFE] - List reminder lists

**Usage Examples:**
```python
# Create a reminder
mission.launch("reminders_create", {
    "name": "Team meeting at 3pm",
    "due_date": "2026-01-28",
    "list": "Work"
})

# Complete a reminder
mission.launch("reminders_complete", {"id": "reminder-id"})

# List all reminders
reminders = mission.launch("reminders_list", {})
```

---

### 📅 Calendar Satellites (4 satellites)

- `calendar_list_calendars` [SAFE] - List calendars
- `calendar_get_events` [SAFE] - Get events in date range
- `calendar_create_event` [MODERATE] - Create event
- `calendar_delete_event` [DANGEROUS] - Delete event

**Usage Examples:**
```python
# Get events for today
events = mission.launch("calendar_get_events", {
    "start_date": "2026-01-27",
    "end_date": "2026-01-28"
})

# Create an event
mission.launch("calendar_create_event", {
    "summary": "Team Meeting",
    "start_date": "2026-01-28 15:00",
    "end_date": "2026-01-28 16:00",
    "calendar": "Work"
})
```

---

### 📧 Mail Satellites (6 satellites)

- `mail_send` [MODERATE] - Send email
- `mail_list_inbox` [SAFE] - List inbox emails
- `mail_get` [SAFE] - Get email content
- `mail_delete` [DANGEROUS] - Delete email
- `mail_mark_as_read` [MODERATE] - Mark as read
- `mail_mark_as_unread` [MODERATE] - Mark as unread

**Usage Examples:**
```python
# List recent emails
emails = mission.launch("mail_list_inbox", {"limit": 10})

# Send an email
mission.launch("mail_send", {
    "to": "user@example.com",
    "subject": "Meeting Notes",
    "body": "Here are the notes from today's meeting..."
})
```

---

### 🌐 Safari Satellites (11 satellites)

- `safari_open` [SAFE] - Open URL
- `safari_get_url` [SAFE] - Get current URL
- `safari_get_text` [SAFE] - Get page text
- `safari_list_tabs` [SAFE] - List all tabs
- `safari_close_tab` [SAFE] - Close tab
- `safari_search` [SAFE] - Search web
- `safari_new_tab` [SAFE] - Open new tab
- `safari_go_back` [SAFE] - Go back
- `safari_go_forward` [SAFE] - Go forward
- `safari_refresh` [SAFE] - Refresh page
- `safari_zoom_in` [SAFE] - Zoom in
- `safari_zoom_out` [SAFE] - Zoom out

**Usage Examples:**
```python
# Open a URL
mission.launch("safari_open", {"url": "https://github.com"})

# Get current URL
url = mission.launch("safari_get_url", {})

# List all tabs
tabs = mission.launch("safari_list_tabs", {})

# Search the web
mission.launch("safari_search", {"query": "Orbit macOS automation"})
```

---

### 🎵 Music Satellites (11 satellites)

- `music_play` [MODERATE] - Start/resume playback
- `music_pause` [MODERATE] - Pause playback
- `music_next` [MODERATE] - Next track
- `music_previous` [MODERATE] - Previous track
- `music_get_current` [SAFE] - Get current track info
- `music_set_volume` [MODERATE] - Set music volume
- `music_get_volume` [SAFE] - Get music volume
- `music_play_track` [MODERATE] - Play specific track
- `music_search` [SAFE] - Search music
- `music_get_playlists` [SAFE] - Get playlists
- `music_shuffle` [MODERATE] - Toggle shuffle

**Usage Examples:**
```python
# Get current track
track = mission.launch("music_get_current", {})
print(f"Playing: {track['name']} by {track['artist']}")

# Play next track
mission.launch("music_next", {})

# Search for a song
results = mission.launch("music_search", {"query": "Beatles"})

# Play specific track
mission.launch("music_play_track", {"name": "Song Name"})
```

---

### 📂 Finder Satellites (6 satellites)

- `finder_open_folder` [SAFE] - Open folder in Finder
- `finder_new_folder` [MODERATE] - Create new folder
- `finder_reveal` [SAFE] - Reveal file in Finder
- `finder_get_selection` [SAFE] - Get selected files
- `finder_empty_trash` [DANGEROUS] - Empty trash
- `finder_get_trash_info` [SAFE] - Get trash info

**Usage Examples:**
```python
# Open Documents folder
mission.launch("finder_open_folder", {"path": "~/Documents"})

# Reveal a file
mission.launch("finder_reveal", {"path": "~/Documents/file.txt"})

# Get selected files
selection = mission.launch("finder_get_selection", {})
```

---

### 👥 Contacts Satellites (4 satellites)

- `contacts_search` [SAFE] - Search contacts
- `contacts_get` [SAFE] - Get contact details
- `contacts_create` [MODERATE] - Create contact
- `contacts_list_all` [SAFE] - List all contacts

**Usage Examples:**
```python
# Search for a contact
contacts = mission.launch("contacts_search", {
    "query": "John"
})

# Get contact details
contact = mission.launch("contacts_get", {"id": "contact-id"})
```

---

### 📶 WiFi Satellites (6 satellites)

- `wifi_connect` [MODERATE] - Connect to network
- `wifi_disconnect` [MODERATE] - Disconnect
- `wifi_list` [SAFE] - List available networks
- `wifi_current` [SAFE] - Get current connection
- `wifi_turn_on` [MODERATE] - Turn on WiFi
- `wifi_turn_off` [MODERATE] - Turn off WiFi

**Usage Examples:**
```python
# List available networks
networks = mission.launch("wifi_list", {})

# Connect to a network
mission.launch("wifi_connect", {"ssid": "NetworkName"})

# Get current connection
current = mission.launch("wifi_current", {})
```

---

### � applications Satellites (8 satellites)

- `app_list` [SAFE] - List installed apps
- `app_launch` [MODERATE] - Launch application
- `app_quit` [MODERATE] - Quit application
- `app_activate` [SAFE] - Bring app to front
- `app_get_running` [SAFE] - Get running apps
- `app_force_quit` [DANGEROUS] - Force quit app
- `app_hide` [MODERATE] - Hide app
- `app_show` [MODERATE] - Show app

**Usage Examples:**
```python
# List all apps
apps = mission.launch("app_list", {})

# Launch Safari
mission.launch("app_launch", {"name": "Safari"})

# Get running apps
running = mission.launch("app_get_running", {})

# Force quit an app
mission.launch("app_force_quit", {"name": "Calculator"})
```

---

## 🔒 Safety System

### 4-Tier Safety Levels

1. **SAFE (51 satellites, 49%)**
   - Read-only operations
   - No system modifications
   - No prompts needed

2. **MODERATE (44 satellites, 42%)**
   - Non-destructive modifications
   - User data changes
   - Prompts recommended

3. **DANGEROUS (7 satellites, 7%)**
   - Destructive operations
   - Data loss potential
   - Explicit approval required

4. **CRITICAL (2 satellites, 2%)**
   - System-level changes
   - Reboot/Shutdown
   - Maximum caution

### Safety Best Practices

```python
from orbit import SafetyShield, SafetyLevel

# Default shield - allows everything
shield = SafetyShield()

# Conservative shield - blocks dangerous operations
conservative = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "prompt",
    SafetyLevel.DANGEROUS: "deny",
    SafetyLevel.CRITICAL: "deny"
})

# Interactive shield - prompts for moderate+
interactive = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "prompt",
    SafetyLevel.DANGEROUS: "prompt",
    SafetyLevel.CRITICAL: "prompt"
})

mission = MissionControl(safety_shield=conservative)
```

---

## 🎯 Common Tasks & Workflows

### Task 1: System Information Gathering

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# Get comprehensive system info
info = mission.launch("system_get_detailed_info", {})
print(f"macOS {info['version']}")
print(f"Host: {info['hostname']}")
print(f"CPU: {info['cpu']}")
print(f"Memory: {info['memory']}")

# Get running apps
apps = mission.launch("app_get_running", {})
print(f"Running apps: {len(apps)}")

# Get current WiFi
wifi = mission.launch("wifi_current", {})
print(f"Connected to: {wifi.get('ssid', 'None')}")
```

### Task 2: Automated Note Creation

```python
# Create a meeting note
mission.launch("notes_create", {
    "title": f"Weeting Notes - {datetime.now().strftime('%Y-%m-%d')}",
    "body": f"""
    <h1>Meeting Summary</h1>
    <h2>Attendees</h2>
    <ul>
        <li>Team Member 1</li>
        <li>Team Member 2</li>
    </ul>
    <h2>Action Items</h2>
    <ol>
        <li>Task 1</li>
        <li>Task 2</li>
    </ol>
    """,
    "folder": "Work"
})
```

### Task 3: File Organization

```python
# Search for all Python files in a directory
py_files = mission.launch("file_search", {
    "path": "~/Projects",
    "query": ".py",
    "file_type": "py"
})

# Create a backup directory
mission.launch("file_create_directory", {
    "path": "~/Documents/Backup"
})

# Copy files to backup
for file_path in py_files:
    filename = os.path.basename(file_path)
    mission.launch("file_copy", {
        "source": file_path,
        "destination": f"~/Documents/Backup/{filename}"
    })
```

### Task 4: Web Research Automation

```python
# Open research URLs
urls = [
    "https://github.com/xiaoxiath/orbit",
    "https://pypi.org/project/orbit-macos/"
]

for url in urls:
    mission.launch("safari_open", {"url": url})
    time.sleep(2)  # Wait for page to load

# Get page content
content = mission.launch("safari_get_text", {})

# Save to notes
mission.launch("notes_create", {
    "title": "Research Notes",
    "body": content[:5000],  # First 5000 chars
    "folder": "Research"
})
```

### Task 5: Music Control

```python
# Get current track
track = mission.launch("music_get_current", {})
print(f"Now playing: {track['name']}")

# Set volume
mission.launch("music_set_volume", {"level": 70})

# Play next
mission.launch("music_next", {})

# Search and play
results = mission.launch("music_search", {"query": "jazz"})
if results:
    mission.launch("music_play_track", {"name": results[0]['name']})
```

---

## 🤖 AI Framework Integration

### OpenAI Functions

```python
from orbit import MissionControl
from orbit.satellites import all_satellites
import openai

mission = MissionControl()
mission.register_constellation(all_satellites)

# Export to OpenAI Functions format
functions = mission.export_to_openai_functions()

# Use with OpenAI API
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Take a screenshot"}],
    functions=functions
)

# Execute function
function_call = response.choices[0].message.function_call
result = mission.launch(
    function_call.name,
    json.loads(function_call.arguments)
)
```

### LangChain Integration

```python
from orbit import MissionControl
from langchain.tools import Tool

mission = MissionControl()
mission.register_constellation(all_satellites)

# Create LangChain tools
tools = [
    Tool(
        name= sat.name,
        func=lambda kwargs, sat=sat: mission.launch(sat.name, kwargs),
        description=sat.description
    )
    for sat in mission.constellation.list_all()
]

# Use with LangChain agent
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent="zero-shot-react-description"
)

result = agent.run("Take a screenshot and save it to Desktop")
```

### Anthropic Claude Integration

```python
from orbit import MissionControl
from anthropic import Anthropic

mission = MissionControl()
mission.register_constellation(all_satellites)

# Export to XML format for Claude
tools_xml = mission.export_to_xml()

client = Anthropic()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=tools_xml,
    messages=[{"role": "user", "content": "Get system info"}]
)

# Execute tool use
if message.stop_reason == "tool_use":
    for block in message.content:
        if block.type == "tool_use":
            result = mission.launch(
                block.name,
                block.input
            )
```

---

## 🐛 Troubleshooting

### Issue: "AppleScript execution failed"

**Cause:** macOS permissions or AppleScript errors

**Solutions:**
```bash
# Grant Terminal/IDE accessibility permissions
# System Settings → Privacy & Security → Accessibility

# Check AppleScript is working
osascript -e 'tell application "System Events" to get name of every process'

# Enable automation permissions
# System Settings → Privacy & Security → Automation
```

### Issue: "Satellite not found"

**Cause:** Satellite not registered

**Solution:**
```python
# List registered satellites
for sat in mission.constellation.list_all():
    print(sat.name)

# Register the missing satellite
from orbit.satellites import system
mission.register(system.system_get_info)
```

### Issue: "Permission denied"

**Cause:** File system permissions

**Solutions:**
```bash
# Check file permissions
ls -la ~/path/to/file

# Fix permissions
chmod 644 ~/path/to/file

# Use absolute paths
mission.launch("file_read", {"path": "/Users/username/file.txt"})
```

### Issue: "Module not found"

**Cause:** Orbit not installed

**Solution:**
```bash
# Reinstall Orbit
pip uninstall orbit-macos
pip install orbit-macos

# Or install from source
cd /path/to/orbit
pip install -e .
```

---

## 📖 CLI Command Reference

### List Commands

```bash
# List all satellites
orbit list

# List by category
orbit list -c system
orbit list -c music
orbit list -c files

# List by safety level
orbit list -s safe
orbit list -s moderate

# Show details
orbit list -d

# Limit output
orbit list -n 50
```

### Search Commands

```bash
# Search by keyword
orbit search safari
orbit search "get info"

# Search in category
orbit search play -c music

# Show details
orbit search create -d
```

### Execution Commands

```bash
# Run satellite
orbit run system_get_info

# Run with parameters
orbit run system_set_volume --level 50

# Run with JSON parameters
orbit run file_write --path '~/test.txt' --content 'Hello'

# Get satellite info
orbit info system_get_info

# Export to formats
orbit export openai-functions > orbit_functions.json
orbit export json-schema > orbit_schema.json
orbit export xml > orbit_tools.xml
```

### Interactive Mode

```bash
# Start REPL
orbit repl

# In REPL:
> list              # List satellites
> search safari     # Search
> run system_get_info  # Execute
> help              # Show help
> exit              # Exit
```

---

## 💡 Best Practices

### 1. Always Check Results

```python
result = mission.launch("file_write", {
    "path": "~/test.txt",
    "content": "Hello"
})

if result.get("success"):
    print("File written successfully")
else:
    print(f"Error: {result.get('error')}")
```

### 2. Handle Errors Gracefully

```python
try:
    result = mission.launch("file_delete", {"path": "~/test.txt"})
except Exception as e:
    print(f"Failed to delete file: {e}")
    # Handle error appropriately
```

### 3. Use Appropriate Safety Levels

```python
# For SAFE operations - no prompt needed
info = mission.launch("system_get_info", {})

# For DANGEROUS operations - confirm first
response = input("Delete file? (yes/no): ")
if response.lower() == "yes":
    mission.launch("file_delete", {"path": "~/test.txt"})
```

### 4. Register Only What You Need

```python
# Bad: Register everything
mission.register_constellation(all_satellites)

# Good: Register only needed category
from orbit.satellites import system_satellites
mission.register_constellation(system_satellites)
```

### 5. Use Absolute Paths When Possible

```python
import os

# Bad: Relative path
mission.launch("file_read", {"path": "~/file.txt"})

# Good: Absolute path
home = os.path.expanduser("~")
mission.launch("file_read", {"path": f"{home}/file.txt"})
```

### 6. Clean Up Resources

```python
# Close MissionControl when done
mission = MissionControl()
try:
    # Do work
    result = mission.launch("system_get_info", {})
finally:
    # Clean up (if needed in future versions)
    pass
```

---

## 🎓 Learning Path

### Beginner (Day 1)
1. Install Orbit
2. Run basic system satellites
3. Understand safety levels
4. Use CLI for simple tasks

### Intermediate (Day 2-3)
1. Write Python scripts
2. Register specific categories
3. Handle errors
4. Create simple workflows

### Advanced (Week 1)
1. Custom safety shields
2. AI framework integration
3. Complex automation workflows
4. Error handling and logging

### Expert (Week 2+)
1. Create custom satellites
2. Optimize performance
3. Build full automation systems
4. Contribute to Orbit

---

## 📚 Additional Resources

- **GitHub**: https://github.com/xiaoxiath/orbit
- **PyPI**: https://pypi.org/project/orbit-macos/
- **Documentation**: https://github.com/xiaoxiath/orbit/tree/main/docs
- **Issue Tracker**: https://github.com/xiaoxiath/orbit/issues

---

## 🚀 Quick Reference Card

### Essential Commands

```python
# Import
from orbit import MissionControl
from orbit.satellites import all_satellites

# Initialize
mission = MissionControl()
mission.register_constellation(all_satellites)

# Execute
result = mission.launch("satellite_name", {"param": "value"})
```

### CLI Quick Start

```bash
# Install
pip install orbit-macos

# Verify
orbit --version

# List
orbit list

# Execute
orbit run system_get_info
```

### Satellite Naming Convention

`{category}_{action}_{optional_object}`

Examples:
- `system_get_info` - Get system info
- `file_list` - List files
- `music_play` - Play music
- `app_launch` - Launch app

---

🛸 **Orbit: Your AI's Bridge to macOS**

*Version 1.0.0 | Total Satellites: 104 | Categories: 12*
