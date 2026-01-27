"""
Anthropic Claude Integration Example for Orbit

This example demonstrates how to use Orbit satellites with Anthropic's Claude API
and its tool use capabilities (also known as function calling).

Requires: pip install anthropic

Claude's tool use API allows Orbit satellites to be called directly during
conversations, enabling powerful macOS automation capabilities.
"""

from orbit import MissionControl
from orbit.satellites.all_satellites import all_satellites
import json
from typing import Optional, Dict, Any

# Try importing Anthropic SDK
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("⚠️  Anthropic package not installed. Install with: pip install anthropic")


# ============================================================================
# Orbit to Claude Tool Converter
# ============================================================================

def satellite_to_claude_tool(satellite):
    """
    Convert an Orbit satellite to Claude tool format.

    Args:
        satellite: Orbit Satellite instance

    Returns:
        Dict in Claude tool format
    """
    # Build input schema from satellite parameters
    properties = {}
    required = []

    for param in satellite.parameters:
        param_schema = {
            "type": param.type,
            "description": param.description
        }

        # Add default value if present
        if hasattr(param, 'default') and param.default is not None:
            param_schema["default"] = param.default

        properties[param.name] = param_schema

        if param.required:
            required.append(param.name)

    # Create Claude tool definition
    tool = {
        "name": satellite.name,
        "description": satellite.description,
        "input_schema": {
            "type": "object",
            "properties": properties
        }
    }

    if required:
        tool["input_schema"]["required"] = required

    return tool


def export_to_claude_tools(mission: MissionControl, categories: Optional[list[str]] = None):
    """
    Export Orbit satellites to Claude tool format.

    Args:
        mission: Configured MissionControl instance
        categories: Optional list of categories to filter

    Returns:
        List of Claude tool definitions
    """
    # Get satellites based on filters
    if categories:
        satellites = []
        for category in categories:
            satellites.extend(mission.constellation.list_by_category(category))
    else:
        satellites = mission.constellation.list_all()

    # Convert to Claude format
    tools = [satellite_to_claude_tool(sat) for sat in satellites]

    print(f"✅ Exported {len(tools)} Claude tools")
    return tools


def execute_claude_tool_use(mission: MissionControl, tool_use_block: Dict[str, Any]):
    """
    Execute a Claude tool use block with Orbit.

    Args:
        mission: Configured MissionControl instance
        tool_use_block: Tool use block from Claude API response

    Returns:
        Result dict with tool result
    """
    tool_name = tool_use_block.name
    tool_input = tool_use_block.input

    try:
        result = mission.launch(tool_name, tool_input)
        return {
            "success": True,
            "tool_use_id": tool_use_block.id,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "tool_use_id": tool_use_block.id,
            "error": str(e)
        }


# ============================================================================
# Example 1: Basic Tool Conversion
# ============================================================================

def example_tool_conversion():
    """Example: Convert Orbit satellites to Claude tools."""
    print("\n" + "="*70)
    print("🤖 Example 1: Orbit to Claude Tool Conversion")
    print("="*70)

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Export to Claude format
    tools = export_to_claude_tools(mission, categories=['system'])

    print(f"\n✅ Converted {len(tools)} satellites to Claude tools")
    print("\n📋 Sample Claude tools:")
    for tool in tools[:3]:
        print(f"\n   Tool: {tool['name']}")
        print(f"   Description: {tool['description'][:60]}...")
        print(f"   Schema: {json.dumps(tool['input_schema'], indent=10)[:150]}...")


# ============================================================================
# Example 2: Claude API Integration
# ============================================================================

def example_claude_api_call(api_key: Optional[str] = None):
    """Example: Complete Claude API integration with Orbit tools."""
    print("\n" + "="*70)
    print("🤖 Example 2: Claude API Integration")
    print("="*70)

    if not HAS_ANTHROPIC:
        print("⚠️  Skipping - Anthropic SDK not installed")
        return

    import os
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Skipping - No ANTHROPIC_API_KEY found")
        print("   Set ANTHROPIC_API_KEY environment variable")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Export safe tools only
    tools = export_to_claude_tools(mission, categories=['system'])

    # Initialize Claude client
    client = anthropic.Anthropic(api_key=api_key)

    print("\n🤖 Calling Claude with Orbit tools...")

    try:
        # Make API call
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            tools=tools[:5],  # Limit for demo
            messages=[
                {
                    "role": "user",
                    "content": "What is my macOS system information?"
                }
            ]
        )

        # Process response
        print("\n📨 Claude Response:")
        if hasattr(message, 'content') and message.content:
            for block in message.content:
                if block.type == "text":
                    print(f"\n💬 Text: {block.text[:200]}...")
                elif block.type == "tool_use":
                    print(f"\n🔧 Tool Use:")
                    print(f"   ID: {block.id}")
                    print(f"   Name: {block.name}")
                    print(f"   Input: {json.dumps(block.input, indent=6)}")

                    # Execute with Orbit
                    result = execute_claude_tool_use(mission, block)
                    print(f"\n✅ Orbit Result:")
                    print(f"   {json.dumps(result, indent=6, default=str)[:300]}...")

    except anthropic.APIError as e:
        print(f"⚠️  API error: {e}")
    except Exception as e:
        print(f"⚠️  Error: {e}")


# ============================================================================
# Example 3: Multi-Turn Conversation
# ============================================================================

def example_multi_turn_conversation(api_key: Optional[str] = None):
    """Example: Multi-turn conversation with tool use."""
    print("\n" + "="*70)
    print("💬 Example 3: Multi-Turn Conversation with Tool Use")
    print("="*70)

    if not HAS_ANTHROPIC:
        print("⚠️  Skipping - Anthropic SDK not installed")
        return

    import os
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  Skipping - No ANTHROPIC_API_KEY found")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    tools = export_to_claude_tools(mission, categories=['system', 'files'])

    client = anthropic.Anthropic(api_key=api_key)

    # Simulate conversation
    messages = [
        {"role": "user", "content": "List the files in my Documents folder"}
    ]

    print("\n💬 Conversation:")
    print("\n👤 User: List the files in my Documents folder")

    try:
        # First call
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            tools=tools[:5],
            messages=messages
        )

        # Check for tool use
        tool_use_found = False
        if hasattr(response, 'content'):
            for block in response.content:
                if block.type == "tool_use":
                    tool_use_found = True
                    print(f"\n🤖 Claude: Let me check that for you...")
                    print(f"   Using tool: {block.name}")

                    # Execute tool
                    result = execute_claude_tool_use(mission, block)

                    # Add tool result to conversation
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result.get("result", result.get("error", "")))
                            }
                        ]
                    })

                    # Second call with tool result
                    print(f"\n🔧 Orbit Result: {str(result)[:100]}...")
                    print("\n🤖 Claude: Processing tool result...")

                    final_response = client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=1024,
                        tools=tools[:5],
                        messages=messages
                    )

                    if hasattr(final_response, 'content'):
                        for final_block in final_response.content:
                            if final_block.type == "text":
                                print(f"\n✅ Final Response: {final_block.text[:200]}...")

                    break

        if not tool_use_found:
            print("\n🤖 Claude: (direct response without tool use)")

    except Exception as e:
        print(f"\n⚠️  Error: {e}")


# ============================================================================
# Example 4: Safety-Filtered Tools
# ============================================================================

def example_safety_filtered_tools():
    """Example: Create Claude tools with safety filtering."""
    print("\n" + "="*70)
    print("🛡️  Example 4: Safety-Filtered Claude Tools")
    print("="*70)

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Export only SAFE tools
    safe_satellites = mission.constellation.list_by_safety("SAFE")
    safe_tools = [satellite_to_claude_tool(sat) for sat in safe_satellites]

    print(f"\n✅ SAFE Tools: {len(safe_tools)}")
    print("\n📋 Sample SAFE tools:")
    for tool in safe_tools[:5]:
        print(f"   • {tool['name']}: {tool['description'][:50]}...")

    # Export MODERATE tools
    moderate_satellites = mission.constellation.list_by_safety("MODERATE")
    moderate_tools = [satellite_to_claude_tool(sat) for sat in moderate_satellites]
    print(f"\n⚠️  MODERATE Tools: {len(moderate_tools)}")


# ============================================================================
# Example 5: Tool Categories
# ============================================================================

def example_categorized_tools():
    """Example: Organize tools by category for Claude."""
    print("\n" + "="*70)
    print("📁 Example 5: Categorized Claude Tools")
    print("="*70)

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    categories = mission.constellation.get_stats()["categories"]

    print(f"\n📊 Available Categories: {len(categories)}")
    print("\n📁 Tools by category:")

    for category in sorted(categories):
        satellites = mission.constellation.list_by_category(category)
        tools = [satellite_to_claude_tool(sat) for sat in satellites]
        print(f"   • {category:15s}: {len(tools):2d} tools")


# ============================================================================
# Example 6: Custom Tool Configurations
# ============================================================================

def example_custom_config():
    """Example: Custom tool configurations for different use cases."""
    print("\n" + "="*70)
    print("⚙️  Example 6: Custom Tool Configurations")
    print("="*70)

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Configuration 1: Productivity tools
    productivity_tools = export_to_claude_tools(
        mission,
        categories=['notes', 'calendar', 'reminders', 'mail']
    )
    print(f"\n📝 Productivity Configuration: {len(productivity_tools)} tools")
    print("   Categories: notes, calendar, reminders, mail")

    # Configuration 2: System tools
    system_tools = export_to_claude_tools(mission, categories=['system'])
    print(f"\n💻 System Configuration: {len(system_tools)} tools")
    print("   Category: system")

    # Configuration 3: Safe read-only tools
    safe_satellites = [
        sat for sat in mission.constellation.list_all()
        if sat.safety_level.name == "SAFE" and
        "get" in sat.name or "list" in sat.name or "search" in sat.name
    ]
    readonly_tools = [satellite_to_claude_tool(sat) for sat in safe_satellites]
    print(f"\n👀 Read-Only Configuration: {len(readonly_tools)} tools")
    print("   Filter: SAFE level, read operations only")


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run all Claude integration examples."""
    print("\n" + "="*70)
    print("🛸  Orbit - Anthropic Claude Integration Demo")
    print("="*70)

    if not HAS_ANTHROPIC:
        print("\n⚠️  Anthropic SDK is not installed!")
        print("\n📦 Install with:")
        print("   pip install anthropic")
        print("\n🔑 Then set your Anthropic API key:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        return

    # Run examples
    example_tool_conversion()
    example_safety_filtered_tools()
    example_categorized_tools()
    example_custom_config()

    # API examples (require API key)
    import os
    if os.getenv("ANTHROPIC_API_KEY"):
        print("\n" + "="*70)
        print("🔑 API Key detected - running live examples...")
        print("="*70)
        example_claude_api_call()
        example_multi_turn_conversation()
    else:
        print("\n" + "="*70)
        print("🔑 No API Key - skipping live API examples")
        print("   Set ANTHROPIC_API_KEY to run Examples 2-3")
        print("="*70)

    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70)

    print("\n📚 Key Features:")
    print("   1. Direct integration with Claude tool use API")
    print("   2. Automatic tool schema generation")
    print("   3. Multi-turn conversation support")
    print("   4. Safety filtering and categorization")
    print("   5. Custom configurations for different use cases")

    print("\n🚀 Advantages of Claude Tool Use:")
    print("   • Native tool use support in Claude API")
    print("   • Multi-step tool calling")
    print("   • Context-aware tool selection")
    print("   • Built-in safety and validation")

    print("\n📖 Documentation:")
    print("   • docs/API_REFERENCE.md - Complete API docs")
    print("   • https://docs.anthropic.com - Anthropic API docs")
    print("   • https://docs.anthropic.com/claude/docs/tool-use - Tool use guide")


if __name__ == "__main__":
    main()
