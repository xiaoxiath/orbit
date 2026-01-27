#!/usr/bin/env python3
"""
Orbit CLI - Command Line Interface for Orbit macOS Automation Toolkit.

This tool provides a convenient way to interact with Orbit satellites
directly from the command line.
"""

import sys
import json
from typing import Optional
import click

# Import Orbit components
try:
    from orbit import MissionControl
    from orbit.satellites.all_satellites import all_satellites
    from orbit.core import SafetyLevel
    ORBIT_AVAILABLE = True
except ImportError:
    ORBIT_AVAILABLE = False
    MissionControl = None


# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'  # Magenta
    OKBLUE = '\033[94m'   # Blue
    OKCYAN = '\033[96m'   # Cyan
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'     # Red
    ENDC = '\033[0m'      # End
    BOLD = '\033[1m'      # Bold
    UNDERLINE = '\033[4m'  # Underline

    @classmethod
    def disable(cls):
        """Disable colors."""
        cls.HEADER = ''
        cls.OKBLUE = ''
        cls.OKCYAN = ''
        cls.OKGREEN = ''
        cls.WARNING = ''
        cls.FAIL = ''
        cls.ENDC = ''
        cls.BOLD = ''
        cls.UNDERLINE = ''


def colorize(text: str, color: str) -> str:
    """Add color to text."""
    return f"{color}{text}{Colors.ENDC}"


def get_mission() -> MissionControl:
    """Get or create MissionControl instance."""
    if not ORBIT_AVAILABLE:
        click.echo(colorize("Error: Orbit is not installed. Please install with: pip install orbit-macos", Colors.FAIL), err=True)
        sys.exit(1)

    mission = MissionControl()
    for satellite in all_satellites:
        mission.register(satellite)
    return mission


def format_satellite_info(satellite, show_details: bool = False) -> str:
    """Format satellite information for display."""
    # Safety level with color
    safety_colors = {
        "safe": Colors.OKGREEN,
        "moderate": Colors.WARNING,
        "dangerous": Colors.FAIL,
        "critical": Colors.FAIL,
    }
    safety_color = safety_colors.get(satellite.safety_level.value, Colors.ENDC)

    # Basic info
    name = colorize(satellite.name, Colors.BOLD + Colors.OKCYAN)
    safety = colorize(f"[{satellite.safety_level.value.upper()}]", safety_color)
    category = colorize(f"{satellite.category}", Colors.OKBLUE)

    info = f"  {name} {safety} {category}"

    if show_details:
        description = colorize(f"\n      Description: {satellite.description}", Colors.ENDC)
        params = f"\n      Parameters: {len(satellite.parameters)}"
        info += f"{description}{params}"

    return info


def format_satellite_table(satellites, show_details: bool = False):
    """Format satellites as a table."""
    if not satellites:
        click.echo(colorize("No satellites found.", Colors.WARNING))
        return

    for sat in satellites:
        click.echo(format_satellite_info(sat, show_details))


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.1", prog_name="orbit")
@click.pass_context
def cli(ctx):
    """
    🛸 Orbit CLI - macOS Automation Toolkit

    Orbit is your AI's bridge to macOS. This CLI tool provides convenient
    access to 100+ satellites for automating macOS applications and system tasks.

    \b
    Examples:
      orbit list                    List all satellites
      orbit search safari            Search for Safari satellites
      orbit run system_get_info      Run a satellite
      orbit interactive              Start interactive mode
      orbit export openai            Export to OpenAI Functions format

    \b
    For more help on each command:
      orbit <command> --help
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(list)


@cli.command()
@click.option('--category', '-c', help='Filter by category')
@click.option('--safety', '-s', type=click.Choice(['safe', 'moderate', 'dangerous', 'critical']), help='Filter by safety level')
@click.option('--details', '-d', is_flag=True, help='Show detailed information')
@click.option('--count', '-n', default=20, help='Number of satellites to show (default: 20)')
def list(category, safety, details, count):
    """
    List all available satellites.

    \b
    Examples:
      orbit list                           # List first 20 satellites
      orbit list -c system                  # List system satellites
      orbit list -s safe                    # List SAFE satellites only
      orbit list -d                         # List with detailed info
      orbit list -n 50                      # List 50 satellites
    """
    mission = get_mission()

    # Get all satellites
    satellites = mission.constellation.list_all()

    # Apply filters
    if category:
        satellites = mission.constellation.list_by_category(category)
        click.echo(colorize(f"\n📋 Satellites in '{category}':\n", Colors.BOLD))

    if safety:
        level = SafetyLevel[safety.upper()]
        satellites = [s for s in satellites if s.safety_level == level]
        click.echo(colorize(f"\n🛡️  {safety.upper()} satellites:\n", Colors.BOLD))

    # Limit results
    satellites = satellites[:count]

    # Show stats
    stats = mission.constellation.get_stats()
    click.echo(colorize(f"Total: {stats['total_satellites']} satellites | Categories: {stats['categories']}\n", Colors.OKCYAN))

    # List satellites
    format_satellite_table(satellites, details)


@cli.command()
@click.argument('query')
@click.option('--category', '-c', help='Search in specific category')
@click.option('--details', '-d', is_flag=True, help='Show detailed information')
def search(query, category, details):
    """
    Search for satellites by name or description.

    \b
    Examples:
      orbit search safari                    # Search for "safari"
      orbit search "get info"               # Search for "get info"
      orbit search music -c music            # Search in music category
      orbit search create -d                 # Search with details
    """
    mission = get_mission()

    # Get satellites
    if category:
        satellites = mission.constellation.list_by_category(category)
    else:
        satellites = mission.constellation.list_all()

    # Search
    results = mission.constellation.search(query)
    if category:
        results = [s for s in results if s in satellites]

    click.echo(colorize(f"\n🔍 Search results for '{query}':\n", Colors.BOLD))

    if results:
        format_satellite_table(results, details)
    else:
        click.echo(colorize("No matching satellites found.", Colors.WARNING))


@cli.command()
@click.argument('satellite_name')
@click.argument('parameters', nargs=-1, type=click.UNPROCESSED)
@click.option('--bypass-shield', is_flag=True, help='Bypass safety checks (not recommended)')
@click.option('--timeout', '-t', default=30, help='Execution timeout in seconds')
def run(satellite_name, parameters, bypass_shield, timeout):
    """
    Run a satellite with parameters.

    \b
    Examples:
      orbit run system_get_info                      # Run without parameters
      orbit run notes_create "My Note"                # Run with positional parameters
      orbit run safari_open "https://github.com"      # Run with URL parameter
      orbit run file_list --path ~/Documents          # Run with named parameter (JSON)
      orbit run system_set_volume '{"level": 50}'      # Run with JSON parameters
    """
    mission = get_mission()

    # Parse parameters
    params = {}
    if parameters:
        if len(parameters) == 1 and parameters[0].startswith('{'):
            # JSON format
            try:
                params = json.loads(parameters[0])
            except json.JSONDecodeError:
                click.echo(colorize("Error: Invalid JSON parameters", Colors.FAIL), err=True)
                sys.exit(1)
        elif '=' in parameters[0]:
            # Key=value format
            for param in parameters:
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
        else:
            # Positional
            params = {"_args": list(parameters)}

    click.echo(colorize(f"\n🚀 Running: {satellite_name}\n", Colors.BOLD))

    try:
        result = mission.launch(
            satellite_name,
            params,
            bypass_shield=bypass_shield
        )

        # Display result
        click.echo(colorize("✅ Success!\n", Colors.OKGREEN))
        try:
            if isinstance(result, dict):
                click.echo(json.dumps(result, indent=2, ensure_ascii=False))
            elif isinstance(result, list):
                for item in result:
                    click.echo(f"  - {item}")
            elif result is None or result == "":
                click.echo(colorize("No output", Colors.OKCYAN))
            else:
                click.echo(str(result))
        except Exception as display_error:
            # Fallback display if formatting fails
            click.echo(str(result))

    except Exception as e:
        click.echo(colorize(f"❌ Error: {str(e)}", Colors.FAIL), err=True)
        sys.exit(1)


@cli.command()
@click.option('--category', '-c', help='Start with specific category')
@click.option('--safe-only', is_flag=True, help='Only show SAFE satellites')
def interactive(category, safe_only):
    """
    Start interactive REPL mode.

    \b
    In interactive mode, you can:
      • Type satellite names to execute
      • Use 'help' for available commands
      • Use 'list' to see satellites
      • Use 'quit' or 'exit' to leave

    \b
    Examples:
      orbit interactive                    # Start interactive mode
      orbit interactive -c system          # Start with system category
      orbit interactive --safe-only        # Show only SAFE satellites
    """
    import readline  # For better input handling

    mission = get_mission()

    click.echo(colorize("""
╔══════════════════════════════════════════════════════════╗
║  🛸  Orbit Interactive Mode                               ║
║                                                          ║
║  Commands:                                               ║
║    • help        - Show this help                        ║
║    • list        - List available satellites             ║
║    • search      - Search satellites                     ║
║    • run <sat>   - Run a satellite                      ║
║    • info <sat>  - Show satellite info                   ║
║    • quit/exit   - Exit interactive mode                 ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""", Colors.OKCYAN))

    while True:
        try:
            # Get input
            prompt = colorize("orbit> ", Colors.BOLD)
            user_input = input(prompt).strip()

            if not user_input:
                continue

            # Parse command
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            # Handle commands
            if command in ['quit', 'exit', 'q']:
                click.echo(colorize("👋 Goodbye!", Colors.OKCYAN))
                break

            elif command == 'help':
                click.echo("""
📖 Available Commands:
  list [options]    - List satellites (same as orbit list)
  search <query>     - Search satellites
  run <sat> [args]   - Run a satellite
  info <sat>         - Show satellite details
  quit/exit          - Exit interactive mode
""")

            elif command == 'list':
                # List satellites
                satellites = mission.constellation.list_all()
                if category:
                    satellites = mission.constellation.list_by_category(category)
                if safe_only:
                    satellites = [s for s in satellites if s.safety_level == SafetyLevel.SAFE]

                click.echo(f"\n📋 Available satellites:\n")
                format_satellite_table(satellites[:20], show_details=False)

            elif command == 'search':
                if not args:
                    click.echo(colorize("Usage: search <query>", Colors.WARNING))
                    continue
                query = ' '.join(args)
                results = mission.constellation.search(query)
                click.echo(f"\n🔍 Results for '{query}':\n")
                format_satellite_table(results[:10], show_details=False)

            elif command == 'info':
                if not args:
                    click.echo(colorize("Usage: info <satellite_name>", Colors.WARNING))
                    continue
                sat_name = args[0]
                satellite = mission.constellation.get(sat_name)
                if not satellite:
                    click.echo(colorize(f"❌ Satellite '{sat_name}' not found", Colors.FAIL))
                    continue

                click.echo(f"\n📋 {satellite.name}\n")
                click.echo(f"  Description: {satellite.description}")
                click.echo(f"  Category: {satellite.category}")
                click.echo(f"  Safety: {satellite.safety_level.value}")
                click.echo(f"  Parameters:")
                if satellite.parameters:
                    for param in satellite.parameters:
                        required = colorize("(required)", Colors.WARNING) if param.required else ""
                        click.echo(f"    • {param.name} ({param.type}) {required}")
                        if param.default:
                            click.echo(f"      Default: {param.default}")
                else:
                    click.echo(f"    (none)")

            elif command == 'run':
                if not args:
                    click.echo(colorize("Usage: run <satellite_name> [args...]", Colors.WARNING))
                    continue

                sat_name = args[0]
                run_args = ' '.join(args[1:]) if len(args) > 1 else "{}"

                try:
                    # Try to parse as JSON
                    try:
                        params = json.loads(run_args) if run_args != "{}" else {}
                    except:
                        params = {"_input": run_args}

                    result = mission.launch(sat_name, params)
                    click.echo(colorize("✅ Success!", Colors.OKGREEN))
                    if isinstance(result, (dict, list)):
                        click.echo(json.dumps(result, indent=2))
                    else:
                        click.echo(str(result))

                except Exception as e:
                    click.echo(colorize(f"❌ Error: {str(e)}", Colors.FAIL))

            else:
                # Try to run as satellite name
                satellite = mission.constellation.get(command)
                if satellite:
                    run_args = ' '.join(args)
                    try:
                        params = json.loads(run_args) if run_args else {}
                        result = mission.launch(command, params)
                        click.echo(colorize("✅ Success!", Colors.OKGREEN))
                        click.echo(str(result))
                    except Exception as e:
                        click.echo(colorize(f"❌ Error: {str(e)}", Colors.FAIL))
                else:
                    click.echo(colorize(f"❌ Unknown command: {command}", Colors.WARNING))
                    click.echo("Type 'help' for available commands")

        except (KeyboardInterrupt, EOFError):
            click.echo(colorize("\n\n👋 Goodbye!", Colors.OKCYAN))
            break
        except Exception as e:
            click.echo(colorize(f"\n❌ Error: {str(e)}", Colors.FAIL))


@cli.command()
@click.argument('format', type=click.Choice(['openai', 'json', 'json-schema', 'stats']))
@click.option('--output', '-o', type=click.Path(), help='Output file path (default: stdout)')
@click.option('--category', '-c', help='Export specific category')
@click.option('--indent', '-i', default=2, help='JSON indentation (default: 2)')
def export(format, output, category, indent):
    """
    Export satellites in various formats.

    \b
    Examples:
      orbit export openai                     # Export to OpenAI Functions format
      orbit export openai -o tools.json       # Save to file
      orbit export json -c system -o sys.json  # Export system satellites
      orbit export stats                       # Show statistics
      orbit export json-schema                 # Export as JSON Schema
    """
    mission = get_mission()

    click.echo(colorize(f"\n📤 Exporting to {format.upper()} format...\n", Colors.BOLD))

    try:
        if format == 'openai':
            # Export to OpenAI Functions format
            if category:
                satellites = mission.constellation.list_by_category(category)
            else:
                satellites = mission.constellation.list_all()

            functions = [sat.to_openai_function() for sat in satellites]
            result = json.dumps(functions, indent=indent, ensure_ascii=False)

            click.echo(colorize(f"✅ Exported {len(functions)} functions", Colors.OKGREEN))

        elif format == 'json':
            # Export to JSON
            if category:
                satellites = mission.constellation.list_by_category(category)
            else:
                satellites = mission.constellation.list_all()

            result = mission.constellation.to_json_schema()

            click.echo(colorize(f"✅ Exported {len(satellites)} satellites", Colors.OKGREEN))

        elif format == 'json-schema':
            # Export as JSON Schema
            if category:
                satellites = mission.constellation.list_by_category(category)
            else:
                satellites = mission.constellation.list_all()

            schema = {
                "title": "Orbit Satellites",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        sat.name: {
                            "type": "object",
                            "description": sat.description,
                            "properties": {
                                param.name: {
                                    "type": param.type,
                                    "description": param.description
                                }
                                for param in satellite.parameters
                            }
                        }
                        for satellite in satellites
                    }
                }
            }

            result = json.dumps(schema, indent=indent, ensure_ascii=False)
            click.echo(colorize(f"✅ Exported schema for {len(satellites)} satellites", Colors.OKGREEN))

        elif format == 'stats':
            # Show statistics
            stats = mission.constellation.get_stats()

            result = {
                "total_satellites": stats["total_satellites"],
                "categories": stats["categories"],
                "by_safety": stats["by_safety"],
                "by_category": {}
            }

            # Get count by category
            categories = mission.constellation.get_categories()
            for cat in categories:
                result["by_category"][cat] = len(mission.constellation.list_by_category(cat))

            result = json.dumps(result, indent=indent, ensure_ascii=False)

            click.echo(colorize("\n📊 Orbit Statistics:", Colors.BOLD))
            click.echo(json.dumps(result, indent=indent, ensure_ascii=False))

        # Write to file or stdout
        if output:
            with open(output, 'w') as f:
                f.write(result)
            click.echo(colorize(f"\n💾 Saved to: {output}", Colors.OKCYAN))
        else:
            if format != 'stats':
                click.echo("\n" + result)

    except Exception as e:
        click.echo(colorize(f"❌ Error: {str(e)}", Colors.FAIL), err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show Orbit version information."""
    click.echo(colorize("""
🛸 Orbit - macOS Automation Toolkit
    """, Colors.OKCYAN))
    click.echo(f"  Version: 1.0.0")
    click.echo(f"  Python: {sys.version.split()[0]}")
    click.echo(f"  Satellites: 104")
    click.echo(f"  Categories: 12")


@cli.command()
@click.option('--category', '-c', help='Test specific category')
def test(category):
    """
    Test Orbit installation and satellite loading.

    \b
    Examples:
      orbit test                           # Test Orbit installation
      orbit test -c system                  # Test system satellites
    """
    click.echo(colorize("\n🧪 Testing Orbit Installation...\n", Colors.BOLD))

    if not ORBIT_AVAILABLE:
        click.echo(colorize("❌ Orbit is not installed!", Colors.FAIL))
        click.echo("Please install with: pip install orbit-macos")
        sys.exit(1)

    try:
        mission = MissionControl()
        click.echo(colorize("✅ MissionControl created", Colors.OKGREEN))

        for satellite in all_satellites:
            mission.register(satellite)

        click.echo(colorize(f"✅ Registered {len(all_satellites)} satellites", Colors.OKGREEN))

        if category:
            sats = mission.constellation.list_by_category(category)
            click.echo(colorize(f"✅ {len(sats)} satellites in '{category}'", Colors.OKGREEN))

        stats = mission.constellation.get_stats()
        click.echo(colorize(f"✅ {stats['total_satellites']} total satellites", Colors.OKGREEN))
        click.echo(colorize(f"✅ {stats['categories']} categories", Colors.OKGREEN))

        click.echo(colorize("\n✨ All tests passed! Orbit is ready to use.\n", Colors.OKGREEN))

    except Exception as e:
        click.echo(colorize(f"❌ Test failed: {str(e)}", Colors.FAIL), err=True)
        sys.exit(1)


def main():
    """Main entry point for CLI."""
    cli()


if __name__ == '__main__':
    main()
