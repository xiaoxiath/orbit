# Orbit Quick Start Guide

<img src="logo.png" alt="Orbit Logo" width="150"/>

> **Get up and running with Orbit in 5 minutes**

---

## 🚀 Installation

### Prerequisites

- macOS 12.0+ (Monterey or later)
- Python 3.10 or higher
- Administrator access (for some AppleScript operations)

### Install via pip

```bash
pip install orbit-macos
```

### Install from source

```bash
git clone https://github.com/yourusername/orbit.git
cd orbit
pip install -e .
```

### Verify Installation

```bash
python -c "from orbit import MissionControl; print('Orbit installed successfully! 🛸')"
```

---

## ⚡ Your First Mission

### Basic Example

Create a file `first_mission.py`:

```python
from orbit import MissionControl
from orbit.satellites import system_satellites

# Initialize mission control
mission = MissionControl()

# Register system satellites
mission.register_constellation(system_satellites)

# Launch your first mission
result = mission.launch(
    "system_get_info",
    parameters={}
)

print(f"macOS Version: {result['version']}")
print(f"Hostname: {result['hostname']}")
print(f"User: {result['username']}")
print(f"Architecture: {result['architecture']}")
```

Run it:

```bash
python first_mission.py
```

Output:

```
macOS Version: 14.0
Hostname: MacBook-Pro
User: astronaut
Architecture: arm64
```

---

## 🛰️ Working with Satellites

### Register Individual Satellites

```python
from orbit import MissionControl
from orbit.satellites.system import info, clipboard

mission = MissionControl()

# Register specific satellites
mission.register(info.system_get_info)
mission.register(clipboard.system_get_clipboard)

# List registered satellites
for satellite in mission.constellation.list_all():
    print(f"🛰️  {satellite.name}: {satellite.description}")
```

### Register All Satellites

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

print(f"Total satellites: {len(mission.constellation.list_all())}")
print(f"Categories: {mission.constellation.get_categories()}")
```

---

## 🛡️ Configure the Safety Shield

### Default Safety Settings

By default, Orbit uses conservative safety settings:

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# Default behavior:
# SAFE operations: Allowed
# MODERATE operations: Require confirmation
# DANGEROUS operations: Require confirmation
# CRITICAL operations: Blocked

mission = MissionControl()  # Uses default shield
```

### Custom Safety Rules

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# Create custom shield
shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "allow",  # Auto-allow moderate ops
        SafetyLevel.DANGEROUS: "deny",   # Block dangerous ops
        SafetyLevel.CRITICAL: "deny"
    }
)

mission = MissionControl(safety_shield=shield)
```

### Add Confirmation Callback

```python
from orbit import SafetyShield, SafetyLevel

def confirm_mission(satellite, parameters):
    """Ask user for confirmation"""
    print(f"\n⚠️  Satellite: {satellite.name}")
    print(f"   Safety Level: {satellite.safety_level.value}")
    print(f"   Parameters: {parameters}")
    return input("Allow this mission? (y/n): ").lower() == "y"

shield = SafetyShield(
    confirmation_callback=confirm_mission
)

mission = MissionControl(safety_shield=shield)
```

---

## 🔌 Framework Integration

### OpenAI Functions

```python
import openai
from orbit import MissionControl
from orbit.satellites import all_satellites

# Setup
mission = MissionControl()
mission.register_constellation(all_satellites)

# Export to OpenAI Functions format
functions = mission.export_openai_functions()

# Use with OpenAI API
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's my macOS version?"}
    ],
    functions=functions,
    function_call="auto"
)

# Execute function call
if response.choices[0].message.function_call:
    result = mission.execute_function_call(
        response.choices[0].message.function_call
    )
    print(f"Result: {result}")
```

### LangChain

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import StructuredTool
from orbit import MissionControl
from orbit.satellites import all_satellites

# Setup
mission = MissionControl()
mission.register_constellation(all_satellites)

# Convert to LangChain tools
langchain_tools = [
    StructuredTool.from_function(
        func=lambda **kwargs: mission.launch(sat.name, kwargs),
        name=sat.name,
        description=sat.description,
    )
    for sat in mission.constellation.list_all()
]

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    langchain_tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Run agent
agent.run("Create a note about my meeting tomorrow at 3pm")
```

---

## 📋 Common Operations

### System Information

```python
from orbit import MissionControl
from orbit.satellites import system_satellites

mission = MissionControl()
mission.register_constellation(system_satellites)

# Get system info
info = mission.launch("system_get_info", {})

# Get clipboard
clipboard = mission.launch("system_get_clipboard", {})

# Send notification
mission.launch("system_send_notification", {
    "title": "Hello from Orbit",
    "message": "Mission accomplished!"
})

# Take screenshot
mission.launch("system_take_screenshot", {
    "path": "~/Desktop/screenshot.png"
})
```

### File Operations

```python
from orbit import MissionControl
from orbit.satellites import file_satellites

mission = MissionControl()
mission.register_constellation(file_satellites)

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

### Notes Operations

```python
from orbit import MissionControl
from orbit.satellites import notes_satellites

mission = MissionControl()
mission.register_constellation(notes_satellites)

# List notes
notes = mission.launch("notes_list", {
    "folder": "Notes"
})

# Create note
mission.launch("notes_create", {
    "title": "Meeting Notes",
    "body": "<h1>Discussion Points</h1><ul><li>Item 1</li><li>Item 2</li></ul>",
    "folder": "Work"
})

# Search notes
results = mission.launch("notes_search", {
    "query": "meeting"
})
```

---

## 🔍 Search and Discovery

### Search Satellites

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

mission = MissionControl()
mission.register_constellation(all_satellites)

# Search by keyword
results = mission.constellation.search("clipboard")

for satellite in results:
    print(f"🛰️  {satellite.name}")
    print(f"   {satellite.description}")
    print(f"   Category: {satellite.category}")
    print()
```

### List by Category

```python
# List all system satellites
system_sats = mission.constellation.list_by_category("system")

for satellite in system_sats:
    print(f"🛰️  {satellite.name}: {satellite.description}")
```

### List by Safety Level

```python
from orbit.satellites import SafetyLevel

# List all safe satellites (read-only)
safe_sats = mission.constellation.list_by_safety(SafetyLevel.SAFE)

print(f"Safe satellites: {len(safe_sats)}")
```

---

## 🐛 Troubleshooting

### Permission Errors

If you get permission errors:

```bash
# Grant Terminal/System Terminal accessibility permissions
# System Settings → Privacy & Security → Accessibility
```

### AppleScript Errors

If AppleScript fails:

1. Check the script syntax
2. Verify the target application is running
3. Check application permissions

```python
from orbit.core.exceptions import AppleScriptError

try:
    result = mission.launch("notes_create", {...})
except AppleScriptError as e:
    print(f"Script error: {e}")
    print(f"Script: {e.script}")
    print(f"Return code: {e.return_code}")
```

### Shield Blocking Operations

```python
from orbit.core.exceptions import ShieldError

try:
    result = mission.launch("file_delete", {"path": "/System/..."})
except ShieldError as e:
    print(f"Safety blocked: {e}")
    # Use bypass_shield=True if you're sure (not recommended)
    # result = mission.launch("file_delete", {...}, bypass_shield=True)
```

---

## 📚 Next Steps

- **[Complete API Reference](API_REFERENCE.md)** - Full API documentation
- **[All Satellites](SATELLITES.md)** - Complete list of 100+ satellites
- **[Security Model](SECURITY.md)** - Deep dive into safety system
- **[Framework Integration Examples](../examples/)** - Code examples for popular frameworks

---

## 💡 Tips

1. **Start with Safe Satellites**: Begin with `SAFE` level satellites to understand the system
2. **Use the Shield**: Always keep the safety shield enabled in production
3. **Read Examples**: Check the `examples/` directory for complete working examples
4. **Handle Errors**: Always wrap mission launches in try-except blocks
5. **Log Missions**: Enable logging to track mission execution

---

**Need Help?**

- GitHub Issues: https://github.com/yourusername/orbit/issues
- Discord: https://discord.gg/orbit
- Email: support@orbit.dev

🛸 Happy orbiting!
