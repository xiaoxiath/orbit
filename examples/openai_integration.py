"""
OpenAI Functions Integration Example for Orbit

This example demonstrates how to use Orbit satellites with OpenAI's function calling API.
Requires: pip install openai

Orbit satellites can be automatically exported to OpenAI Functions format,
enabling seamless integration with GPT-3.5 and GPT-4.
"""

from orbit import MissionControl
from orbit.satellites.all_satellites import all_satellites
import json
from typing import Optional

# For OpenAI SDK v1.0+
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️  OpenAI package not installed. Install with: pip install openai")


def create_orbit_mission():
    """Create and configure MissionControl with all satellites."""
    mission = MissionControl()

    # Register all satellites
    for satellite in all_satellites:
        mission.register(satellite)

    print(f"✅ Registered {len(mission.constellation.list_all())} satellites")
    return mission


def export_to_openai_functions(mission: MissionControl, categories: Optional[list[str]] = None):
    """
    Export Orbit satellites to OpenAI Functions format.

    Args:
        mission: Configured MissionControl instance
        categories: Optional list of categories to filter (e.g., ['system', 'files'])

    Returns:
        List of OpenAI function definitions
    """
    # Export all or filtered satellites
    if categories:
        functions = []
        for category in categories:
            category_sats = mission.constellation.list_by_category(category)
            for satellite in category_sats:
                functions.append(satellite.to_openai_function())
    else:
        functions = mission.export_openai_functions()

    print(f"📋 Exported {len(functions)} function definitions")
    return functions


def execute_function_call(mission: MissionControl, function_name: str, arguments: dict):
    """
    Execute an Orbit satellite based on OpenAI function call.

    Args:
        mission: Configured MissionControl instance
        function_name: Name of the function/satellite to call
        arguments: Parameters dict from OpenAI response

    Returns:
        Result from satellite execution
    """
    try:
        result = mission.launch(function_name, arguments)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# Example 1: Basic Function Calling
# ============================================================================

def example_basic_function_calling():
    """Basic example with system information satellites."""
    print("\n" + "="*70)
    print("📡 Example 1: Basic Function Calling")
    print("="*70)

    if not HAS_OPENAI:
        print("⚠️  Skipping - OpenAI not installed")
        return

    # Initialize
    mission = create_orbit_mission()

    # Export system satellites only
    system_functions = export_to_openai_functions(mission, categories=['system'])

    print("\n📤 System Functions Available:")
    for func in system_functions[:3]:  # Show first 3
        print(f"   • {func['name']}: {func['description'][:60]}...")

    # Simulate OpenAI function call
    print("\n🤖 Simulating OpenAI Function Call:")
    print("   User: 'What's my macOS version?'")
    print("   Assistant: Calling system_get_info...")

    # This is what OpenAI would return
    simulated_function_call = {
        "name": "system_get_info",
        "arguments": {}
    }

    # Execute with Orbit
    result = execute_function_call(
        mission,
        simulated_function_call["name"],
        simulated_function_call["arguments"]
    )

    print(f"   Result: {json.dumps(result, indent=6)}")


# ============================================================================
# Example 2: Multi-Step Conversation
# ============================================================================

def example_multi_step_conversation():
    """Example showing multi-step conversation with function calls."""
    print("\n" + "="*70)
    print("📡 Example 2: Multi-Step Conversation")
    print("="*70)

    if not HAS_OPENAI:
        print("⚠️  Skipping - OpenAI not installed")
        return

    mission = create_orbit_mission()
    functions = export_to_openai_functions(mission, categories=['notes', 'calendar'])

    # Simulate conversation
    conversation = [
        {
            "role": "user",
            "content": "Create a note about my meeting tomorrow at 2pm"
        },
        {
            "role": "assistant",
            "function_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "notes_create",
                        "arguments": '{"name": "Meeting Tomorrow", "body": "Meeting at 2pm"}'
                    }
                }
            ]
        },
        {
            "role": "function",
            "name": "notes_create",
            "content": "success"
        }
    ]

    print("\n💬 Simulated Conversation:")
    for i, msg in enumerate(conversation):
        if msg["role"] == "user":
            print(f"\n   [{i}] User: {msg['content']}")
        elif msg["role"] == "assistant" and "function_calls" in msg:
            func = msg["function_calls"][0]["function"]
            print(f"\n   [{i}] Assistant: Calling {func['name']}")
            print(f"       Arguments: {func['arguments']}")
        elif msg["role"] == "function":
            print(f"\n   [{i}] Function Result: {msg['content']}")


# ============================================================================
# Example 3: Complete OpenAI Integration
# ============================================================================

def example_complete_integration(api_key: Optional[str] = None):
    """
    Complete example with actual OpenAI API call.

    Args:
        api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
    """
    print("\n" + "="*70)
    print("📡 Example 3: Complete OpenAI Integration")
    print("="*70)

    if not HAS_OPENAI:
        print("⚠️  Skipping - OpenAI not installed")
        return

    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        print(f"⚠️  Could not initialize OpenAI client: {e}")
        print("   Set OPENAI_API_KEY environment variable to run this example")
        return

    # Setup Orbit
    mission = create_orbit_mission()
    functions = export_to_openai_functions(mission, categories=['system'])

    print("\n🤖 Calling OpenAI GPT...")

    try:
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful macOS assistant."},
                {"role": "user", "content": "What's my system information?"}
            ],
            functions=functions[:5],  # Limit for demo
            function_call="auto",
            temperature=0
        )

        message = response.choices[0].message

        # Check if function call needed
        if message.function_call:
            func_name = message.function_call.name
            func_args = json.loads(message.function_call.arguments)

            print(f"\n📞 GPT called: {func_name}")
            print(f"   Arguments: {func_args}")

            # Execute with Orbit
            result = execute_function_call(mission, func_name, func_args)
            print(f"\n✅ Orbit Result: {json.dumps(result, indent=6, default=str)}")
        else:
            print(f"\n💬 GPT Response: {message.content}")

    except Exception as e:
        print(f"⚠️  API call failed: {e}")


# ============================================================================
# Example 4: Filtered Functions by Category
# ============================================================================

def example_filtered_functions():
    """Example showing how to filter functions by category and safety."""
    print("\n" + "="*70)
    print("📡 Example 4: Filtered Functions by Category")
    print("="*70)

    mission = create_orbit_mission()

    # Export only SAFE functions
    safe_functions = []
    for satellite in mission.constellation.list_by_safety("SAFE"):
        safe_functions.append(satellite.to_openai_function())

    print(f"\n✅ SAFE Functions: {len(safe_functions)}")
    print("\n📋 Sample SAFE functions:")
    for func in safe_functions[:5]:
        print(f"   • {func['name']}: {func['description'][:50]}...")

    # Export only file operations
    file_functions = export_to_openai_functions(mission, categories=['files'])
    print(f"\n📁 File Functions: {len(file_functions)}")
    print("\n📋 File operations:")
    for func in file_functions:
        print(f"   • {func['name']}: {func['description'][:50]}...")


# ============================================================================
# Example 5: Custom Function Schema
# ============================================================================

def example_custom_schema():
    """Example showing custom schema modifications for OpenAI."""
    print("\n" + "="*70)
    print("📡 Example 5: Custom Function Schema")
    print("="*70)

    mission = create_orbit_mission()

    # Get functions and customize
    functions = mission.export_openai_functions()

    # Add custom metadata
    for func in functions:
        func["orbit_category"] = func.get("name", "").split("_")[0]
        func["orbit_safe"] = True  # Mark as Orbit-validated

    print("\n🔧 Enhanced Functions:")
    print(f"\n   Total: {len(functions)}")
    print(f"   Categories: {len(set(f['orbit_category'] for f in functions))}")

    print("\n📋 Sample enhanced function:")
    if functions:
        sample = functions[0]
        print(f"   Name: {sample.get('name')}")
        print(f"   Category: {sample.get('orbit_category')}")
        print(f"   Validated: {sample.get('orbit_safe')}")
        print(f"   Description: {sample.get('description', '')[:60]}...")


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("🛸  Orbit - OpenAI Functions Integration Demo")
    print("="*70)

    # Run examples
    example_basic_function_calling()
    example_multi_step_conversation()
    example_filtered_functions()
    example_custom_schema()

    # Complete integration (requires API key)
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("\n" + "="*70)
        print("🔑 API Key detected - running complete integration...")
        print("="*70)
        example_complete_integration(api_key)
    else:
        print("\n" + "="*70)
        print("🔑 No API Key found - skipping live API call")
        print("   Set OPENAI_API_KEY to run Example 3")
        print("="*70)

    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70)

    print("\n📚 Key Takeaways:")
    print("   1. Orbit satellites export directly to OpenAI Functions format")
    print("   2. Use to_openai_function() for individual satellites")
    print("   3. Use export_openai_functions() for all satellites")
    print("   4. Filter by category or safety level as needed")
    print("   5. Execute function calls with mission.launch()")

    print("\n🚀 Next Steps:")
    print("   • Set OPENAI_API_KEY environment variable")
    print("   • Run: python examples/openai_integration.py")
    print("   • Integrate with your OpenAI-powered agents")

    print("\n📖 Documentation:")
    print("   • docs/API_REFERENCE.md - Complete API docs")
    print("   • docs/QUICKSTART.md - Quick start guide")
    print("   • examples/openai_functions.py - More examples")


if __name__ == "__main__":
    main()
