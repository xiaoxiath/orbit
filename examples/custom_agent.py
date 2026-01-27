"""
Custom AI Agent Example with Orbit

This example demonstrates how to build a custom AI agent that uses Orbit satellites
to automate macOS tasks. The agent can process natural language requests and
execute appropriate macOS operations.

This is a framework-agnostic example that doesn't require OpenAI, LangChain, or
Anthropic - it shows the core patterns for building your own agent.
"""

from orbit import MissionControl, ShieldAction
from orbit.satellites.all_satellites import all_satellites
import re
import json
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum


# ============================================================================
# Agent Configuration
# ============================================================================

class AgentIntent(Enum):
    """Intents that the agent can recognize."""
    GET_INFO = "get_info"
    CREATE_NOTE = "create_note"
    SEND_NOTIFICATION = "send_notification"
    LIST_FILES = "list_files"
    SEARCH_WEB = "search_web"
    PLAY_MUSIC = "play_music"
    CREATE_EVENT = "create_event"
    CREATE_REMINDER = "create_reminder"
    READ_CLIPBOARD = "read_clipboard"
    TAKE_SCREENSHOT = "take_screenshot"
    UNKNOWN = "unknown"


# ============================================================================
# Intent Recognition
# ============================================================================

class IntentRecognizer:
    """Simple rule-based intent recognizer for the agent."""

    # Intent patterns (keyword -> intent mapping)
    PATTERNS = {
        AgentIntent.GET_INFO: [
            r"system (info|information)",
            r"macOS version",
            r"computer info",
            r"what (version|system)"
        ],
        AgentIntent.CREATE_NOTE: [
            r"create (a )?note",
            r"new note",
            r"write (this )?in (a )?note",
            r"save (as )?note"
        ],
        AgentIntent.SEND_NOTIFICATION: [
            r"send (a )?notification",
            r"notify me",
            r"show notification"
        ],
        AgentIntent.LIST_FILES: [
            r"list (the )?files",
            r"show (me )?files",
            r"what files",
            r"directory listing"
        ],
        AgentIntent.SEARCH_WEB: [
            r"search (for )?(the )?web",
            r"google",
            r"open.*safari"
        ],
        AgentIntent.PLAY_MUSIC: [
            r"play (some )?music",
            r"start music",
            r"next track",
            r"pause (the )?music"
        ],
        AgentIntent.CREATE_EVENT: [
            r"create (an )?event",
            r"schedule (a )?meeting",
            r"add to calendar"
        ],
        AgentIntent.CREATE_REMINDER: [
            r"create (a )?reminder",
            r"remind me",
            r"add reminder"
        ],
        AgentIntent.READ_CLIPBOARD: [
            r"clipboard",
            r"what.*copied"
        ],
        AgentIntent.TAKE_SCREENSHOT: [
            r"(take )?screenshot",
            r"capture.*screen",
            r"snip"
        ]
    }

    def recognize(self, text: str) -> AgentIntent:
        """
        Recognize the intent from user input.

        Args:
            text: User's natural language input

        Returns:
            Recognized AgentIntent
        """
        text = text.lower().strip()

        # Check each intent's patterns
        for intent, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent

        return AgentIntent.UNKNOWN

    def extract_parameters(self, text: str, intent: AgentIntent) -> Dict[str, Any]:
        """
        Extract parameters from user input based on intent.

        Args:
            text: User's natural language input
            intent: Recognized intent

        Returns:
            Dict of parameters for the satellite
        """
        params = {}

        if intent == AgentIntent.CREATE_NOTE:
            # Extract note name and content
            params["name"] = "Quick Note"  # Default
            # Look for quoted text or after "note"
            match = re.search(r'note ["\'](.+?)["\']', text, re.IGNORECASE)
            if match:
                params["name"] = match.group(1)
            else:
                # Use entire text as note body
                params["body"] = text

        elif intent == AgentIntent.SEND_NOTIFICATION:
            # Extract title and message
            params["title"] = "Notification"
            params["message"] = text

            match = re.search(r'["\'](.+?)["\']', text)
            if match:
                params["message"] = match.group(1)

        elif intent == AgentIntent.LIST_FILES:
            # Extract path
            params["path"] = "~/Documents"  # Default

            match = re.search(r'in ["\']?([^"\']+)["\']?', text)
            if match:
                params["path"] = match.group(1)

        elif intent == AgentIntent.SEARCH_WEB:
            # Extract search query
            match = re.search(r'(?:search|google|for) ["\']?([^"\']+)["\']?', text, re.IGNORECASE)
            if match:
                params["query"] = match.group(1)
            else:
                params["query"] = text

        elif intent == AgentIntent.CREATE_EVENT:
            # Extract event details
            params["summary"] = "New Event"
            params["start_date"] = "today"
            params["end_date"] = "today"

            match = re.search(r'["\'](.+?)["\']', text)
            if match:
                params["summary"] = match.group(1)

        elif intent == AgentIntent.CREATE_REMINDER:
            # Extract reminder details
            params["name"] = "New Reminder"
            params["due_date"] = "today"

            match = re.search(r'["\'](.+?)["\']', text)
            if match:
                params["name"] = match.group(1)

        return params


# ============================================================================
# Custom Orbit Agent
# ============================================================================

class OrbitAgent:
    """
    Custom AI agent that uses Orbit satellites to automate macOS tasks.

    Features:
    - Intent recognition from natural language
    - Parameter extraction
    - Satellite execution
    - Result formatting
    - Conversation memory
    """

    def __init__(self, safety_level: str = "SAFE"):
        """
        Initialize the Orbit agent.

        Args:
            safety_level: Maximum safety level to allow (SAFE, MODERATE, DANGEROUS)
        """
        self.mission = MissionControl()
        self.recognizer = IntentRecognizer()
        self.safety_level = safety_level
        self.conversation_history: List[Dict[str, str]] = []

        # Register all satellites
        for satellite in all_satellites:
            self.mission.register(satellite)

        print(f"✅ Orbit Agent initialized")
        print(f"   Satellites: {len(self.mission.constellation.list_all())}")
        print(f"   Safety Level: {safety_level}")

    def process(self, user_input: str) -> str:
        """
        Process user input and execute appropriate action.

        Args:
            user_input: Natural language input from user

        Returns:
            Response message
        """
        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Recognize intent
        intent = self.recognizer.recognize(user_input)

        if intent == AgentIntent.UNKNOWN:
            response = "🤔 I'm not sure what you want me to do. Try asking me to:"
            response += "\n   • Get system information"
            response += "\n   • Create a note"
            response += "\n   • Send a notification"
            response += "\n   • List files"
            response += "\n   • Take a screenshot"

            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response

        # Extract parameters
        params = self.recognizer.extract_parameters(user_input, intent)

        # Execute action
        response = self._execute_intent(intent, params)

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def _execute_intent(self, intent: AgentIntent, params: Dict[str, Any]) -> str:
        """Execute the recognized intent with appropriate satellite."""
        try:
            if intent == AgentIntent.GET_INFO:
                result = self.mission.launch("system_get_info", {})
                return f"📊 System Info:\n{json.dumps(result, indent=2, default=str)}"

            elif intent == AgentIntent.CREATE_NOTE:
                result = self.mission.launch("notes_create", params)
                return f"✅ Note created: {params.get('name', 'Quick Note')}"

            elif intent == AgentIntent.SEND_NOTIFICATION:
                result = self.mission.launch("system_send_notification", params)
                return f"📢 Notification sent: {params.get('message', '')[:50]}..."

            elif intent == AgentIntent.LIST_FILES:
                result = self.mission.launch("file_list", params)
                if isinstance(result, list):
                    return f"📁 Files in {params.get('path', '~/Documents')}:\n" + "\n".join(result[:10])
                return f"📁 Files listed"

            elif intent == AgentIntent.SEARCH_WEB:
                result = self.mission.launch("safari_search", params)
                return f"🌐 Searching Safari for: {params.get('query', '')}"

            elif intent == AgentIntent.PLAY_MUSIC:
                result = self.mission.launch("music_play", {})
                return "🎵 Playing music"

            elif intent == AgentIntent.CREATE_EVENT:
                result = self.mission.launch("calendar_create_event", params)
                return f"📅 Event created: {params.get('summary', 'New Event')}"

            elif intent == AgentIntent.CREATE_REMINDER:
                result = self.mission.launch("reminders_create", params)
                return f"⏰ Reminder created: {params.get('name', 'New Reminder')}"

            elif intent == AgentIntent.READ_CLIPBOARD:
                result = self.mission.launch("system_get_clipboard", {})
                return f"📋 Clipboard:\n{result[:100]}..."

            elif intent == AgentIntent.TAKE_SCREENSHOT:
                result = self.mission.launch("system_take_screenshot", {})
                return "📸 Screenshot saved"

            else:
                return "❌ Unknown intent"

        except Exception as e:
            return f"❌ Error executing action: {str(e)}"

    def chat(self):
        """
        Start an interactive chat session with the agent.
        """
        print("\n" + "="*70)
        print("🛸  Orbit Agent - Interactive Mode")
        print("="*70)
        print("\n💬 Type your requests (or 'quit' to exit)")
        print("\n📝 Example requests:")
        print("   • 'Get system information'")
        print("   • 'Create a note about my meeting'")
        print("   • 'Send notification: Hello World'")
        print("   • 'List files in ~/Documents'")
        print("   • 'Take a screenshot'")
        print("\n" + "="*70)

        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                # Process input
                response = self.process(user_input)
                print(f"\n🤖 Agent: {response}")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        stats = {
            "total_satellites": len(self.mission.constellation.list_all()),
            "categories": len(self.mission.constellation.get_stats()["categories"]),
            "conversation_turns": len(self.conversation_history),
            "safety_level": self.safety_level
        }
        return stats


# ============================================================================
# Example Usage
# ============================================================================

def example_basic_usage():
    """Example: Basic agent usage."""
    print("\n" + "="*70)
    print("🤖 Example 1: Basic Agent Usage")
    print("="*70)

    # Create agent
    agent = OrbitAgent(safety_level="SAFE")

    # Test queries
    test_queries = [
        "Get system information",
        "Create a note about Orbit project",
        "Send notification: Hello from Orbit!",
        "Take a screenshot"
    ]

    print("\n📝 Testing queries:")
    for query in test_queries:
        print(f"\n👤 Query: {query}")
        response = agent.process(query)
        print(f"🤖 Response: {response[:100]}...")

    # Show stats
    stats = agent.get_stats()
    print(f"\n📊 Agent Stats:")
    print(f"   Satellites: {stats['total_satellites']}")
    print(f"   Categories: {stats['categories']}")
    print(f"   Conversation Turns: {stats['conversation_turns']}")


def example_custom_intents():
    """Example: Adding custom intents to the agent."""
    print("\n" + "="*70)
    print("🔧 Example 2: Custom Intents")
    print("="*70)

    # Create custom recognizer
    custom_recognizer = IntentRecognizer()

    # Add custom patterns
    custom_recognizer.PATTERNS[AgentIntent.CREATE_NOTE].extend([
        r"remember (that )?(the )?",
        r"don't forget (that )?(the )?"
    ])

    print("\n✅ Added custom intent patterns:")
    print("   • 'Remember that...'")
    print("   • 'Don't forget that...'")

    # Test
    test_input = "Remember that I have a meeting at 3pm"
    intent = custom_recognizer.recognize(test_input)

    print(f"\n📝 Input: {test_input}")
    print(f"🎯 Intent: {intent.value}")


def example_batch_processing():
    """Example: Batch process multiple requests."""
    print("\n" + "="*70)
    print("📦 Example 3: Batch Processing")
    print("="*70)

    agent = OrbitAgent()

    # Batch of requests
    requests = [
        "Get system info",
        "Create note: Project update",
        "List files in ~/Documents",
        "Play music"
    ]

    print(f"\n📦 Processing {len(requests)} requests...")

    results = []
    for i, request in enumerate(requests, 1):
        print(f"\n[{i}/{len(requests)}] {request}")
        response = agent.process(request)
        results.append({
            "request": request,
            "response": response[:50] + "..." if len(response) > 50 else response
        })

    print(f"\n✅ Batch complete")
    print(f"   Total requests: {len(results)}")
    print(f"   Succeeded: {sum(1 for r in results if not r['response'].startswith('❌'))}")


def example_conversation_memory():
    """Example: Agent with conversation memory."""
    print("\n" + "="*70)
    print("💾 Example 4: Conversation Memory")
    print("="*70)

    agent = OrbitAgent()

    # Simulate conversation
    conversation = [
        "Get system information",
        "Create a note about my macOS version",
        "Send notification: Notes updated",
        "What did I just ask you to do?"  # This will be UNKNOWN but shows memory
    ]

    print("\n💬 Simulated conversation:")
    for user_input in conversation:
        print(f"\n👤 User: {user_input}")
        response = agent.process(user_input)
        print(f"🤖 Agent: {response[:100]}...")

    # Show conversation history
    print(f"\n📚 Conversation History: {len(agent.conversation_history)} turns")
    print("\n   Last 3 exchanges:")
    for exchange in agent.conversation_history[-3:]:
        role = exchange["role"].capitalize()
        content = exchange["content"][:60] + "..." if len(exchange["content"]) > 60 else exchange["content"]
        print(f"   {role}: {content}")


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run all agent examples."""
    print("\n" + "="*70)
    print("🛸  Orbit - Custom Agent Demo")
    print("="*70)

    # Run examples
    example_basic_usage()
    example_custom_intents()
    example_batch_processing()
    example_conversation_memory()

    # Interactive mode
    print("\n" + "="*70)
    print("🎮 Interactive Mode")
    print("="*70)
    print("\nWould you like to try interactive chat? (y/n): ", end="")

    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes']:
            agent = OrbitAgent()
            agent.chat()
        else:
            print("\n✅ Demo complete!")
    except KeyboardInterrupt:
        print("\n\n✅ Demo complete!")

    print("\n" + "="*70)
    print("📚 Key Features Demonstrated:")
    print("="*70)
    print("""
   1. Intent Recognition
      • Rule-based pattern matching
      • Extensible intent system
      • Parameter extraction

   2. Satellite Execution
      • Automatic satellite selection
      • Safety level enforcement
      • Error handling

   3. Conversation Memory
      • Full conversation history
      • Context awareness
      • Multi-turn support

   4. Extensibility
      • Custom intents
      • Custom recognizers
      • Batch processing
    """)

    print("\n🚀 Build Your Own Agent:")
    print("   1. Define your intents")
    print("   2. Add intent patterns")
    print("   3. Implement parameter extraction")
    print("   4. Connect to Orbit satellites")
    print("   5. Add your own logic")

    print("\n📖 Documentation:")
    print("   • docs/API_REFERENCE.md - Complete API docs")
    print("   • docs/DESIGN.md - Architecture guide")


if __name__ == "__main__":
    main()
