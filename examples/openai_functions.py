"""Example: Using Orbit with OpenAI Functions."""

import openai
from orbit import MissionControl
from orbit.satellites import system


def main():
    """Demonstrate OpenAI Functions integration."""
    # Initialize Mission Control
    mission = MissionControl()

    # Register system satellites
    mission.register_constellation([
        system.system_get_info,
        system.system_send_notification,
    ])

    # Export to OpenAI Functions format
    functions = mission.export_openai_functions()

    print("🛸 Orbit - OpenAI Functions Integration\n")
    print("📋 Exported functions:")
    for func in functions:
        print(f"   - {func['function']['name']}: {func['function']['description']}")

    print("\n🤖 Calling OpenAI...")
    # Note: This requires OPENAI_API_KEY to be set
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's my macOS version?"}
            ],
            functions=functions,
            function_call="auto"
        )

        # Execute function call if present
        msg = response.choices[0].message
        if msg.function_call:
            print(f"\n🚀 Launching: {msg.function_call.name}")
            result = mission.execute_function_call(msg.function_call)
            print(f"✅ Result: {result}")
        else:
            print(f"\n💬 Response: {msg.content}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Note: Make sure OPENAI_API_KEY is set")


if __name__ == "__main__":
    main()
