"""
Orbit CLI - Command Line Interface Examples

This file demonstrates how to use the Orbit CLI tool.
"""

# ============================================================================
# Basic Usage Examples
# ============================================================================

# 1. List all satellites
# $ orbit list

# 2. List satellites in a specific category
# $ orbit list -c system
# $ orbit list -c safari

# 3. List only SAFE satellites
# $ orbit list -s safe

# 4. List with detailed information
# $ orbit list -d

# 5. List more satellites
# $ orbit list -n 50

# ============================================================================
# Search Examples
# ============================================================================

# 1. Search by name
# $ orbit search safari

# 2. Search by description
# $ orbit search "get info"

# 3. Search in specific category
# $ orbit search create -c notes

# 4. Search with details
# $ orbit search music -d

# ============================================================================
# Run Examples
# ============================================================================

# 1. Run satellite without parameters
# $ orbit run system_get_info

# 2. Run with positional parameters
# $ orbit run notes_create "My Meeting Note"

# 3. Run with URL parameter
# $ orbit run safari_open "https://github.com"

# 4. Run with JSON parameters
# $ orbit run file_list '{"path": "~/Documents"}'
# $ orbit run notes_create '{"name": "Test", "body": "Content"}'

# 5. Run with key=value format
# $ orbit run system_set_volume level=50

# ============================================================================
# Interactive Mode Examples
# ============================================================================

# 1. Start interactive mode
# $ orbit interactive

# In interactive mode:
# orbit> list                    # List satellites
# orbit> search safari            # Search satellites
# orbit> run system_get_info      # Run a satellite
# orbit> info system_get_info     # Show satellite info
# orbit> help                     # Show help
# orbit> quit                     # Exit

# 2. Start with category filter
# $ orbit interactive -c system

# 3. Start with safe-only satellites
# $ orbit interactive --safe-only

# ============================================================================
# Export Examples
# ============================================================================

# 1. Export to OpenAI Functions format (stdout)
# $ orbit export openai

# 2. Export and save to file
# $ orbit export openai -o tools.json
# $ orbit export json -o satellites.json

# 3. Export specific category
# $ orbit export openai -c system -o system_tools.json

# 4. Export as JSON Schema
# $ orbit export json-schema

# 5. Show statistics
# $ orbit export stats

# ============================================================================
# Other Commands
# ============================================================================

# 1. Show version
# $ orbit version

# 2. Test installation
# $ orbit test

# 3. Get help
# $ orbit --help
# $ orbit list --help
# $ orbit run --help

# ============================================================================
# Practical Examples
# ============================================================================

# Example 1: Daily workflow automation
# $ orbit run notes_create "Daily Notes - $(date +%Y-%m-%d)" 'Today I focused on:'
# $ orbit run calendar_create_event "Team Standup" start_date="today 10:00" end_date="today 10:30"
# $ orbit run system_send_notification '{"title": "Meeting", "message": "Starting in 5 minutes"}'

# Example 2: Web research workflow
# $ orbit run safari_open "https://github.com"
# $ orbit run safari_search "Orbit macOS automation"
# $ orbit run safari_get_text
# $ orbit run notes_create "Research: Orbit Automation"

# Example 3: File management
# $ orbit run file_list '{"path": "~/Downloads"}'
# $ orbit run file_create_directory '{"name": "Archive", "location": "~/Documents"}'
# $ orbit run file_move '{"source": "~/Downloads/file.txt", "destination": "~/Documents/Archive/file.txt"}'

# Example 4: System information
# $ orbit run system_get_info
# $ orbit run system_get_detailed_info
# $ orbit run file_get_info '{"path": "/System"}'

# Example 5: Export for AI integration
# $ orbit export openai -o orbit_tools.json
# Then use the JSON with OpenAI API or LangChain

# ============================================================================
# Advanced Usage
# ============================================================================

# 1. Chain commands
# $ orbit run system_get_info && orbit run notes_create "System Info Collected"
# $ orbit run file_list path=~/Desktop | orbit run notes_create -

# 2. Use with shell scripts
# #!/bin/bash
# orbit run system_get_info > system_info.json
# orbit run notes_create "Backup $(date +%F)" "$(cat system_info.json)"

# 3. Filter and process
# $ orbit list -s safe | grep -i music | awk '{print $2}' | xargs -I {} orbit info {}

# 4. Export and use with other tools
# $ orbit export openai | jq '.[] | select(.function.name | contains("system"))'
# $ orbit export stats | jq '.by_category'

# ============================================================================
# Tips and Tricks
# ============================================================================

# Tip 1: Use aliases for common tasks
# Add to ~/.bashrc or ~/.zshrc:
# alias orbit-sys='orbit run system_get_info'
# alias orbit-note='orbit run notes_create'
# alias orbit-safari='orbit run safari_open'

# Tip 2: Create shell scripts
# #!/bin/bash
# # daily_backup.sh
# orbit run notes_create "Daily Backup $(date +%F)"
# orbit run file_create_directory name=Backup_$(date +%F)
# orbit run file_copy source=~/Documents destination=~/Backup_$(date +%F)/Documents

# Tip 3: Use with cron
# Add to crontab:
# 0 9 * * * /usr/local/bin/orbit run system_send_notification '{"title": "Morning Briefing", "message": "Check your calendar"}'
# 0 18 * * * /usr/local/bin/orbit run notes_create "Evening Notes" "End of day summary"

# Tip 4: Combine with macOS tools
# $ orbit run system_get_info | pbcopy  # Copy to clipboard
# $ orbit run safari_list_tabs | grep -i github

# Tip 5: Export and edit
# $ orbit export openai -o tools.json
# $ vim tools.json  # Edit as needed
# $ orbit run system_send_notification "$(cat tools.json | jq -r '.[0].function.description')"

# ============================================================================
# Troubleshooting
# ============================================================================

# Problem: Command not found
# Solution: Make sure Orbit is installed
# $ pip install orbit-macos --upgrade
# $ which orbit

# Problem: Satellite not found
# Solution: Check satellite name with search
# $ orbit search <partial_name>

# Problem: Permission denied
# Solution: Some satellites require permissions
# $ orbit run <satellite> --bypass-shield  # Not recommended!

# Problem: AppleScript execution failed
# Solution: Make sure you're on macOS
# $ orbit test

# ============================================================================
# Getting Help
# ============================================================================

# General help
# $ orbit --help

# Command-specific help
# $ orbit list --help
# $ orbit run --help
# $ orbit interactive --help

# Show satellite info
# $ orbit interactive
# orbit> info <satellite_name>

# ============================================================================
# Exit Codes
# ============================================================================

# 0: Success
# 1: General error
# 2: Satellite not found
# 3: Validation error
# 4: Execution error

# Check exit code in scripts:
# $ orbit run system_get_info
# echo $?

# ============================================================================
# Version Info
# ============================================================================

# Show Orbit CLI version
# $ orbit version

# Expected output:
# 🛸 Orbit - macOS Automation Toolkit
#   Version: 1.0.0
#   Python: 3.10
#   Satellites: 104
#   Categories: 12
