# Orbit API Reference

> **Version:** 1.0.0
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Core Classes](#core-classes)
   - [MissionControl](#missioncontrol)
   - [Satellite](#satellite)
   - [Constellation](#constellation)
   - [Launcher](#launcher)
   - [SafetyShield](#safetyshield)
2. [Data Structures](#data-structures)
   - [SafetyLevel](#safetylevel)
   - [ShieldAction](#shieldaction)
   - [SatelliteParameter](#satelliteparameter)
3. [Exception Classes](#exception-classes)
4. [Result Parsers](#result-parsers)
5. [Utility Functions](#utility-functions)

---

## Core Classes

### MissionControl

Main entry point for Orbit. Manages satellite constellation and mission execution.

```python
from orbit import MissionControl

mission = MissionControl()
mission.register_constellation(all_satellites)
result = mission.launch("system_get_info", {})
```

#### Constructor

```python
MissionControl(
    safety_shield: Optional[SafetyShield] = None,
    launcher: Optional[Launcher] = None
) -> None
```

**Parameters:**
- `safety_shield` - Optional safety shield. Defaults to a shield with default rules.
- `launcher` - Optional launcher instance. Defaults to a new Launcher instance.

**Example:**
```python
from orbit import MissionControl, SafetyShield, SafetyLevel

# Create with custom shield
shield = SafetyShield(rules={
    SafetyLevel.SAFE: "allow",
    SafetyLevel.MODERATE: "allow"
})
mission = MissionControl(safety_shield=shield)
```

#### Methods

##### register

```python
register(satellite: Satellite) -> None
```

Register a single satellite.

**Parameters:**
- `satellite` - Satellite instance to register

**Raises:**
- `ValueError` - If satellite already registered

**Example:**
```python
from orbit.satellites.system import info
mission.register(info.system_get_info)
```

##### register_constellation

```python
register_constellation(satellites: List[Satellite]) -> None
```

Register multiple satellites at once.

**Parameters:**
- `satellites` - List of satellites to register

**Example:**
```python
from orbit.satellites import all_satellites
mission.register_constellation(all_satellites)
```

##### launch

```python
launch(
    satellite_name: str,
    parameters: dict,
    bypass_shield: bool = False
) -> Any
```

Launch a mission (execute a satellite).

**Parameters:**
- `satellite_name` - Name of the satellite to launch
- `parameters` - Mission parameters dict
- `bypass_shield` - Skip safety checks (not recommended)

**Returns:**
- Mission result (type depends on satellite)

**Raises:**
- `SatelliteNotFoundError` - If satellite not found
- `ShieldError` - If safety check fails
- `AppleScriptError` - If script execution fails

**Example:**
```python
result = mission.launch(
    "system_get_info",
    parameters={}
)
print(result["version"])
```

##### export_openai_functions

```python
export_openai_functions() -> List[dict]
```

Export all registered satellites to OpenAI Functions format.

**Returns:**
- List of OpenAI Function format dicts

**Example:**
```python
functions = mission.export_openai_functions()

import openai
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's my macOS version?"}],
    functions=functions
)
```

##### execute_function_call

```python
execute_function_call(function_call: dict) -> Any
```

Execute an OpenAI function call response.

**Parameters:**
- `function_call` - OpenAI function_call dict from response

**Returns:**
- Mission result

**Example:**
```python
response = openai.chat.completions.create(...)
if response.choices[0].message.function_call:
    result = mission.execute_function_call(
        response.choices[0].message.function_call
    )
```

#### Properties

##### constellation

```python
mission.constellation: Constellation
```

Access the constellation registry.

**Example:**
```python
all_satellites = mission.constellation.list_all()
system_satellites = mission.constellation.list_by_category("system")
```

---

### Satellite

Represents a single automation tool (satellite).

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel

satellite = Satellite(
    name="example_tool",
    description="An example satellite",
    category="system",
    parameters=[...],
    safety_level=SafetyLevel.SAFE,
    applescript_template='return "hello"'
)
```

#### Constructor

```python
Satellite(
    name: str,
    description: str,
    category: str,
    parameters: List[SatelliteParameter],
    safety_level: SafetyLevel,
    applescript_template: str,
    result_parser: Optional[Callable] = None,
    examples: List[dict] = None,
    version: str = "1.0.0",
    author: str = ""
)
```

**Parameters:**
- `name` - Unique identifier (snake_case)
- `description` - LLM-readable description
- `category` - Category (system, files, notes, etc.)
- `parameters` - List of parameter definitions
- `safety_level` - Safety classification
- `applescript_template` - Jinja2 template for AppleScript
- `result_parser` - Optional result parser function
- `examples` - Optional list of usage examples
- `version` - Satellite version
- `author` - Satellite author

#### Methods

##### to_openai_function

```python
to_openai_function() -> dict
```

Convert satellite to OpenAI Function format.

**Returns:**
- OpenAI Function format dict

##### to_dict

```python
to_dict() -> dict
```

Convert satellite to dictionary format.

**Returns:**
- Satellite data dict

---

### Constellation

Registry for managing the satellite constellation.

```python
from orbit.core import Constellation

constellation = Constellation()
constellation.register(satellite)
all_satellites = constellation.list_all()
```

#### Methods

##### register

```python
register(satellite: Satellite) -> None
```

Register a satellite.

**Parameters:**
- `satellite` - Satellite to register

**Raises:**
- `ValueError` - If satellite already exists

##### unregister

```python
unregister(name: str) -> None
```

Unregister a satellite.

**Parameters:**
- `name` - Satellite name

**Raises:**
- `ValueError` - If satellite not found

##### get

```python
get(name: str) -> Optional[Satellite]
```

Get satellite by name.

**Parameters:**
- `name` - Satellite name

**Returns:**
- Satellite instance or None

##### list_all

```python
list_all() -> List[Satellite]
```

Get all registered satellites.

**Returns:**
- List of all satellites

##### list_by_category

```python
list_by_category(category: str) -> List[Satellite]
```

Get satellites by category.

**Parameters:**
- `category` - Category name

**Returns:**
- List of satellites in category

##### list_by_safety

```python
list_by_safety(safety_level: SafetyLevel) -> List[Satellite]
```

Get satellites by safety level.

**Parameters:**
- `safety_level` - Safety level

**Returns:**
- List of satellites with given safety level

##### search

```python
search(query: str) -> List[Satellite]
```

Search satellites by name or description.

**Parameters:**
- `query` - Search query

**Returns:**
- List of matching satellites

##### to_openai_functions

```python
to_openai_functions() -> List[dict]
```

Export all satellites to OpenAI Functions format.

**Returns:**
- List of OpenAI Function dicts

##### to_json_schema

```python
to_json_schema() -> str
```

Export all satellites as JSON Schema string.

**Returns:**
- JSON Schema string

##### get_categories

```python
get_categories() -> List[str]
```

Get all category names.

**Returns:**
- List of category names

##### get_stats

```python
get_stats() -> dict
```

Get constellation statistics.

**Returns:**
- Dict with total_satellites, categories, by_safety

---

### Launcher

Executes AppleScript for satellites.

```python
from orbit.core import Launcher, SafetyShield

shield = SafetyShield()
launcher = Launcher(safety_shield=shield)
result = launcher.launch(satellite, parameters)
```

#### Constructor

```python
Launcher(
    safety_shield: Optional[SafetyShield] = None,
    timeout: int = 30,
    retry_on_failure: bool = False,
    max_retries: int = 3
)
```

**Parameters:**
- `safety_shield` - Optional safety shield
- `timeout` - Script execution timeout in seconds
- `retry_on_failure` - Whether to retry on failure
- `max_retries` - Maximum retry attempts

#### Methods

##### launch

```python
launch(
    satellite: Satellite,
    parameters: dict,
    bypass_shield: bool = False
) -> Any
```

Execute a satellite.

**Parameters:**
- `satellite` - Satellite to execute
- `parameters` - Execution parameters
- `bypass_shield` - Skip safety checks

**Returns:**
- Execution result

**Raises:**
- `ShieldError` - If safety check fails
- `AppleScriptError` - If execution fails

##### launch_async

```python
async launch_async(
    satellite: Satellite,
    parameters: dict
) -> Any
```

Execute a satellite asynchronously.

**Parameters:**
- `satellite` - Satellite to execute
- `parameters` - Execution parameters

**Returns:**
- Execution result

**Example:**
```python
import asyncio

result = await launcher.launch_async(satellite, parameters)
```

---

### SafetyShield

Validates and controls mission execution.

```python
from orbit.core import SafetyShield, SafetyLevel

shield = SafetyShield(
    rules={
        SafetyLevel.SAFE: "allow",
        SafetyLevel.MODERATE: "confirm"
    }
)
```

#### Constructor

```python
SafetyShield(
    rules: Optional[Dict[SafetyLevel, ShieldAction]] = None,
    confirmation_callback: Optional[Callable] = None,
    protected_paths: Optional[List[Path]] = None,
    dangerous_commands: Optional[List[str]] = None
)
```

**Parameters:**
- `rules` - Safety level to action mapping
- `confirmation_callback` - User confirmation function
- `protected_paths` - List of protected system paths
- `dangerous_commands` - List of dangerous command patterns

#### Methods

##### validate

```python
validate(satellite: Satellite, parameters: dict) -> bool
```

Validate mission safety.

**Parameters:**
- `satellite` - Satellite to validate
- `parameters` - Mission parameters

**Returns:**
- True if safe

**Raises:**
- `ShieldError` - If validation fails

##### add_protected_path

```python
add_protected_path(path: str) -> None
```

Add a protected path.

**Parameters:**
- `path` - Path string to protect

##### remove_protected_path

```python
remove_protected_path(path: str) -> None
```

Remove a protected path.

**Parameters:**
- `path` - Path string to unprotect

---

## Data Structures

### SafetyLevel

Enum for satellite safety levels.

```python
from orbit.core import SafetyLevel

SafetyLevel.SAFE       # Read-only, no side effects
SafetyLevel.MODERATE   # Create/modify operations
SafetyLevel.DANGEROUS  # Delete operations
SafetyLevel.CRITICAL   # System-level operations
```

**Values:**
- `SAFE` - Safe operations (read-only)
- `MODERATE` - Moderate risk (create/modify)
- `DANGEROUS` - Dangerous operations (delete)
- `CRITICAL` - Critical operations (system-level)

### ShieldAction

Enum for shield actions.

```python
from orbit.core import ShieldAction

ShieldAction.ALLOW                   # Allow operation
ShieldAction.DENY                    # Deny operation
ShieldAction.REQUIRE_CONFIRMATION    # Require user confirmation
```

### SatelliteParameter

Parameter definition for satellites.

```python
from orbit.core import SatelliteParameter

param = SatelliteParameter(
    name="file_path",
    type="string",
    description="Path to the file",
    required=True,
    default=None
)
```

#### Constructor

```python
SatelliteParameter(
    name: str,
    type: str,
    description: str,
    required: bool = True,
    default: Any = None,
    enum: Optional[list] = None
)
```

**Parameters:**
- `name` - Parameter name
- `type` - Parameter type (string, integer, boolean, object, array)
- `description` - Parameter description
- `required` - Whether parameter is required
- `default` - Default value
- `enum` - Optional list of allowed values

---

## Exception Classes

### OrbitError

Base exception for all Orbit errors.

```python
from orbit.core.exceptions import OrbitError
```

### ShieldError

Raised when safety check fails.

```python
from orbit.core.exceptions import ShieldError

try:
    mission.launch("dangerous_operation", {...})
except ShieldError as e:
    print(f"Safety blocked: {e}")
```

### AppleScriptError

Raised when AppleScript execution fails.

```python
from orbit.core.exceptions import AppleScriptError

try:
    mission.launch("notes_create", {...})
except AppleScriptError as e:
    print(f"Script error: {e}")
    print(f"Return code: {e.return_code}")
    print(f"Script: {e.script}")
```

**Attributes:**
- `script` - The failed script
- `return_code` - AppleScript return code

### AppleScriptTimeoutError

Raised when script execution times out.

```python
from orbit.core.exceptions import AppleScriptTimeoutError
```

### AppleScriptPermissionError

Raised when AppleScript lacks permissions.

```python
from orbit.core.exceptions import AppleScriptPermissionError
```

### AppleScriptSyntaxError

Raised when AppleScript has syntax errors.

```python
from orbit.core.exceptions import AppleScriptSyntaxError
```

### SatelliteNotFoundError

Raised when satellite not found in constellation.

```python
from orbit.core.exceptions import SatelliteNotFoundError

try:
    mission.launch("nonexistent_satellite", {})
except SatelliteNotFoundError as e:
    print(f"Satellite not found: {e}")
```

### ParameterValidationError

Raised when parameter validation fails.

```python
from orbit.core.exceptions import ParameterValidationError
```

### TemplateRenderingError

Raised when template rendering fails.

```python
from orbit.core.exceptions import TemplateRenderingError
```

---

## Result Parsers

### JSONResultParser

Parse JSON output from AppleScript.

```python
from orbit.parsers import JSONResultParser

parser = JSONResultParser()
result = parser.parse('{"key": "value"}')
# result = {"key": "value"}
```

### DelimitedResultParser

Parse delimited output.

```python
from orbit.parsers import DelimitedResultParser

parser = DelimitedResultParser(delimiter="|", field_names=["name", "age"])
result = parser.parse("John|30")
# result = {"name": "John", "age": "30"}
```

### RegexResultParser

Parse output using regex.

```python
from orbit.parsers import RegexResultParser

parser = RegexResultParser(
    pattern=r"Name: (\w+), Age: (\d+)",
    group_names=["name", "age"]
)
result = parser.parse("Name: John, Age: 30")
# result = {"name": "John", "age": "30"}
```

### BooleanResultParser

Parse boolean output.

```python
from orbit.parsers import BooleanResultParser

parser = BooleanResultParser()
result = parser.parse("true")
# result = True
```

---

## Utility Functions

### check_permissions

Check macOS permissions for Orbit.

```python
from orbit.utils import check_permissions

permissions = check_permissions()
for perm, granted in permissions.items():
    print(f"{perm}: {'✅' if granted else '❌'}")
```

**Returns:**
- Dict mapping permission names to granted status

### get_system_info

Get Orbit and system information.

```python
from orbit.utils import get_system_info

info = get_system_info()
print(f"Orbit version: {info['orbit_version']}")
print(f"macOS version: {info['macos_version']}")
```

**Returns:**
- Dict with Orbit and system information

---

## Complete Examples

### Basic Usage

```python
from orbit import MissionControl
from orbit.satellites import all_satellites

# Initialize
mission = MissionControl()
mission.register_constellation(all_satellites)

# Launch mission
result = mission.launch("system_get_info", {})
print(f"macOS {result['version']}")
```

### Custom Safety

```python
from orbit import MissionControl, SafetyShield, SafetyLevel

def confirm(satellite, params):
    return input(f"Allow {satellite.name}? (y/n): ") == "y"

shield = SafetyShield(
    rules={SafetyLevel.MODERATE: "confirm"},
    confirmation_callback=confirm
)

mission = MissionControl(safety_shield=shield)
```

### Custom Satellite

```python
from orbit.core import Satellite, SatelliteParameter, SafetyLevel
from orbit.parsers import DelimitedResultParser

my_satellite = Satellite(
    name="get_current_time",
    description="Get current time from macOS",
    category="system",
    parameters=[],
    safety_level=SafetyLevel.SAFE,
    applescript_template="""
    tell application "System Events"
        set currentTime to current date
        set timeString to time string of currentTime
    end tell
    return timeString
    """,
    result_parser=lambda x: {"time": x}
)

mission.register(my_satellite)
```

### Async Execution

```python
import asyncio
from orbit import MissionControl

async def main():
    mission = MissionControl()
    mission.register_constellation(all_satellites)

    # Launch multiple missions concurrently
    results = await asyncio.gather(
        mission.launcher.launch_async(sat1, params1),
        mission.launcher.launch_async(sat2, params2),
        mission.launcher.launch_async(sat3, params3)
    )

    return results

asyncio.run(main())
```

---

**API Version:** 1.0.0
**Last Updated:** 2026-01-27
