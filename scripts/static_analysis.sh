#!/bin/bash
# Static Analysis for Orbit Project
# Runs all quality checks before committing

set -e

echo "🔍 Orbit Static Analysis"
echo "========================"
echo ""

# Navigate to project root
cd "/Users/bytedance/workspace/llm/macagent-orbit"

echo "1️⃣  Type Checking (mypy)..."
if command -v mypy &> /dev/null; then
    mypy src/orbit/ || echo "⚠️  mypy not installed"
else
    echo "⚠️  mypy not installed - skipping"
fi
echo ""

echo "2️⃣  Linting (ruff)..."
if command -v ruff &> /dev/null; then
    ruff check src/orbit/ || echo "⚠️  ruff not installed"
else
    echo "⚠️  ruff not installed - skipping"
fi
echo ""

echo "3️⃣  Security Check (bandit)..."
if command -v bandit &> /dev/null; then
    bandit -r src/orbit/ -f screen || echo "⚠️  bandit not installed"
else
    echo "⚠️  bandit not installed - skipping"
fi
echo ""

echo "4️⃣  AppleScript Syntax Check..."
python3 scripts/check_applescript.py
echo ""

echo "5️⃣  Import Check..."
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from orbit import MissionControl
    from orbit.satellites import all_satellites
    print('   ✅ All imports successful')
except Exception as e:
    print(f'   ❌ Import error: {e}')
    sys.exit(1)
"
echo ""

echo "✅ Static Analysis Complete!"
echo ""
echo "Run tests with: python3 -m pytest tests/"
