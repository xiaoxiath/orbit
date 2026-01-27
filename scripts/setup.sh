#!/bin/bash

# Orbit Development Setup Script

set -e

echo "🛸 Orbit - Development Setup"
echo ""

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "⚠️  Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "📦 Installing dependencies..."
poetry install

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start developing:"
echo "   poetry shell    # Activate virtual environment"
echo "   pytest          # Run tests"
echo "   python examples/basic_usage.py  # Run example"
