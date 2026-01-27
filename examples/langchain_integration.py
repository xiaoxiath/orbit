"""
LangChain Integration Example for Orbit

This example demonstrates how to integrate Orbit satellites with LangChain.
Requires: pip install langchain langchain-openai

Orbit satellites can be wrapped as LangChain tools, enabling seamless
integration with LangChain agents and chains.
"""

from orbit import MissionControl
from orbit.satellites.all_satellites import all_satellites
import json
from typing import Optional, Type
from pydantic import BaseModel, Field

# Try importing LangChain
try:
    from langchain.tools import BaseTool, StructuredTool
    from langchain.schema import AIMessage, HumanMessage
    from langchain.agents import AgentExecutor, create_openai_functions_agent
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    print("⚠️  LangChain not installed. Install with: pip install langchain langchain-openai")


# ============================================================================
# Orbit to LangChain Tool Adapter
# ============================================================================

class OrbitTool(BaseTool):
    """Adapter for wrapping Orbit satellites as LangChain tools."""

    name: str = ""
    description: str = ""
    mission: MissionControl = None
    satellite_name: str = ""

    def _run(self, **kwargs) -> str:
        """Run the Orbit satellite synchronously."""
        try:
            result = self.mission.launch(self.satellite_name, kwargs)
            return json.dumps({"success": True, "result": result}, default=str)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    async def _arun(self, **kwargs) -> str:
        """Run the Orbit satellite asynchronously."""
        # Orbit's launch_async can be used here
        return self._run(**kwargs)


def create_orbit_tools(
    mission: MissionControl,
    categories: Optional[list[str]] = None,
    safety_level: Optional[str] = None
) -> list[BaseTool]:
    """
    Create LangChain tools from Orbit satellites.

    Args:
        mission: Configured MissionControl instance
        categories: Filter by categories (e.g., ['system', 'files'])
        safety_level: Filter by safety level ('SAFE', 'MODERATE', etc.)

    Returns:
        List of LangChain BaseTool instances
    """
    tools = []

    # Get satellites based on filters
    if categories:
        satellites = []
        for category in categories:
            satellites.extend(mission.constellation.list_by_category(category))
    elif safety_level:
        satellites = mission.constellation.list_by_safety(safety_level)
    else:
        satellites = mission.constellation.list_all()

    # Convert each satellite to a LangChain tool
    for satellite in satellites:
        tool = OrbitTool(
            name=satellite.name,
            description=f"{satellite.description}\nParameters: {json.dumps({p.name: p.description for p in satellite.parameters}, indent=2)}",
            mission=mission,
            satellite_name=satellite.name
        )
        tools.append(tool)

    return tools


# ============================================================================
# Example 1: Basic LangChain Tool
# ============================================================================

def example_basic_tool():
    """Example: Create and use a basic Orbit tool with LangChain."""
    print("\n" + "="*70)
    print("🔗 Example 1: Basic LangChain Tool")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites[:10]:  # Register first 10
        mission.register(satellite)

    # Create LangChain tool
    system_tools = create_orbit_tools(mission, categories=['system'])

    print(f"\n✅ Created {len(system_tools)} LangChain tools")
    print("\n📋 Available Tools:")
    for tool in system_tools[:3]:
        print(f"   • {tool.name}: {tool.description[:60]}...")

    # Use a tool
    if system_tools:
        tool = system_tools[0]
        print(f"\n🔧 Using tool: {tool.name}")
        result = tool._run()
        print(f"   Result: {result[:200]}...")


# ============================================================================
# Example 2: Orbit Agent with LangChain
# ============================================================================

def example_orbit_agent(api_key: Optional[str] = None):
    """Example: Create an AI agent using Orbit tools with LangChain."""
    print("\n" + "="*70)
    print("🤖 Example 2: Orbit Agent with LangChain")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    import os
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Skipping - No OPENAI_API_KEY found")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Create tools (system and file operations only for safety)
    tools = create_orbit_tools(mission, categories=['system', 'files'])

    print(f"\n✅ Agent configured with {len(tools)} tools")

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        temperature=0,
        api_key=api_key
    )

    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful macOS assistant. Use the available tools to help the user."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    # Create agent
    print("\n🤖 Creating LangChain agent...")
    try:
        agent = create_openai_functions_agent(llm, tools[:5], prompt)  # Limit tools for demo
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools[:5],
            verbose=True,
            handle_parsing_errors=True
        )

        # Test query
        print("\n📝 Test Query: 'What is my system information?'")
        result = agent_executor.invoke({"input": "What is my system information?"})
        print(f"\n✅ Agent Response: {result['output']}")

    except Exception as e:
        print(f"⚠️  Agent execution failed: {e}")


# ============================================================================
# Example 3: Custom Tool Chain
# ============================================================================

def example_custom_chain():
    """Example: Build a custom chain with Orbit tools."""
    print("\n" + "="*70)
    print("⛓️  Example 3: Custom Tool Chain")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    from langchain.chains import LLMChain
    from langchain.output_parsers import PydanticOutputParser
    from pydantic import BaseModel, Field

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    tools = create_orbit_tools(mission, categories=['system'])

    # Define output schema
    class SystemInfo(BaseModel):
        """System information schema."""
        os_version: str = Field(description="macOS version")
        hostname: str = Field(description="Computer hostname")
        model: str = Field(description="Hardware model")

    # Create parser
    parser = PydanticOutputParser(pydantic_object=SystemInfo)

    print("\n✅ Custom chain configured")
    print(f"   Tools: {len(tools)}")
    print(f"   Output Schema: SystemInfo")


# ============================================================================
# Example 4: Filtered Tools by Safety
# ============================================================================

def example_safety_filtered_tools():
    """Example: Create tools with safety filtering."""
    print("\n" + "="*70)
    print("🛡️  Example 4: Safety-Filtered Tools")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Create SAFE tools only
    safe_tools = create_orbit_tools(mission, safety_level="SAFE")

    print(f"\n✅ SAFE Tools: {len(safe_tools)}")
    print("\n📋 Sample SAFE tools:")
    for tool in safe_tools[:5]:
        print(f"   • {tool.name}: {tool.description[:50]}...")

    # Create MODERATE tools
    moderate_tools = create_orbit_tools(mission, safety_level="MODERATE")
    print(f"\n⚠️  MODERATE Tools: {len(moderate_tools)}")


# ============================================================================
# Example 5: Structured Tools with Schema
# ============================================================================

def example_structured_tools():
    """Example: Create structured tools with proper schema."""
    print("\n" + "="*70)
    print("📐 Example 5: Structured Tools with Schema")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Get a satellite with parameters
    note_satellites = mission.constellation.list_by_category("notes")
    if note_satellites:
        notes_create = note_satellites[2]  # notes_create

        print(f"\n📝 Satellite: {notes_create.name}")
        print(f"   Description: {notes_create.description}")
        print(f"   Parameters:")
        for param in notes_create.parameters:
            print(f"      • {param.name} ({param.type}): {param.description}")

        # Create structured tool
        def notes_create_func(name: str, body: str = "", folder: str = "") -> str:
            """Create a new note."""
            try:
                result = mission.launch("notes_create", {
                    "name": name,
                    "body": body,
                    "folder": folder
                })
                return json.dumps({"success": True, "result": result})
            except Exception as e:
                return json.dumps({"success": False, "error": str(e)})

        structured_tool = StructuredTool.from_function(
            func=notes_create_func,
            name="notes_create",
            description="Create a new note in the Notes app"
        )

        print(f"\n✅ Created structured tool")
        print(f"   Name: {structured_tool.name}")
        print(f"   Args Schema: {structured_tool.args_schema}")


# ============================================================================
# Example 6: Tool Categories
# ============================================================================

def example_category_tools():
    """Example: Organize tools by category."""
    print("\n" + "="*70)
    print("📁 Example 6: Tools by Category")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("⚠️  Skipping - LangChain not installed")
        return

    # Setup Orbit
    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)

    # Get all categories
    categories = mission.constellation.get_stats()["categories"]

    print(f"\n📊 Available Categories: {len(categories)}")
    print("\n📁 Tools per category:")

    tool_counts = {}
    for category in categories:
        tools = create_orbit_tools(mission, categories=[category])
        tool_counts[category] = len(tools)
        print(f"   • {category}: {len(tools)} tools")

    print(f"\n✅ Total tools across all categories: {sum(tool_counts.values())}")


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run all LangChain integration examples."""
    print("\n" + "="*70)
    print("🛸  Orbit - LangChain Integration Demo")
    print("="*70)

    if not HAS_LANGCHAIN:
        print("\n⚠️  LangChain is not installed!")
        print("\n📦 Install with:")
        print("   pip install langchain langchain-openai")
        print("\n🔑 Then set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-key-here'")
        return

    # Run examples
    example_basic_tool()
    example_safety_filtered_tools()
    example_category_tools()
    example_structured_tools()
    example_custom_chain()

    # Agent example (requires API key)
    import os
    if os.getenv("OPENAI_API_KEY"):
        print("\n" + "="*70)
        print("🔑 API Key detected - running agent example...")
        print("="*70)
        example_orbit_agent()
    else:
        print("\n" + "="*70)
        print("🔑 No API Key - skipping agent example")
        print("   Set OPENAI_API_KEY to run Example 2")
        print("="*70)

    print("\n" + "="*70)
    print("✅ Demo Complete!")
    print("="*70)

    print("\n📚 Key Features:")
    print("   1. OrbitTool adapter wraps satellites as LangChain tools")
    print("   2. Filter by category, safety level, or custom criteria")
    print("   3. Create agents with Orbit tools")
    print("   4. Build custom chains with Orbit functions")
    print("   5. Structured tools with proper schema validation")

    print("\n🚀 Use Cases:")
    print("   • macOS automation agents")
    print("   • File management workflows")
    print("   • System monitoring chains")
    print("   • Cross-application automation")

    print("\n📖 Documentation:")
    print("   • docs/API_REFERENCE.md - Complete API docs")
    print("   • https://python.langchain.com - LangChain docs")


if __name__ == "__main__":
    main()
