#!/bin/bash
# Install Orbit CLI Bash completion

set -e

echo "🛸  Installing Orbit CLI Bash completion..."
echo ""

# Copy completion file to completions directory
COMPLETIONS_DIR="/usr/local/etc/bash_completion.d"
COMPLETION_FILE="scripts/completion.bash"

if [ -f "$COMPLETION_FILE" ]; then
    # Create completions directory if it doesn't exist
    if [ ! -d "$COMPLETIONS_DIR" ]; then
        echo "📁 Creating completions directory: $COMPLETIONS_DIR"
        sudo mkdir -p "$COMPLETIONS_DIR"
    fi

    # Copy completion file
    echo "📋 Copying completion script to $COMPLETIONS_DIR..."
    sudo cp "$COMPLETION_FILE" "$COMPLETIONS_DIR/orbit"

    echo "✅ Bash completion installed!"
    echo ""
    echo "📝 To enable completion in your current shell:"
    echo "   source /usr/local/etc/bash_completion.d/orbit"
    echo ""
    echo "📝 To enable permanently, add to ~/.bashrc or ~/.bash_profile:"
    echo "   echo 'source /usr/local/etc/bash_completion.d/orbit' >> ~/.bashrc"
    echo ""
    echo "🔄 Restart your shell or run:"
    echo "   source ~/.bashrc"
else
    echo "❌ Error: completion file not found at $COMPLETION_FILE"
    exit 1
fi
