#!/bin/bash
# Orbit Test Runner Script
# Runs all tests and generates coverage report

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🛸  Orbit Test Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if pytest is available
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}pytest not found. Installing...${NC}"
    pip install pytest pytest-cov pytest-asyncio pytest-mock
fi

echo -e "${GREEN}Running Orbit test suite...${NC}"
echo ""

# Run tests with coverage
pytest tests/ \
    --cov=orbit \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    -v \
    --tb=short \
    "$@"

# Exit status
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Coverage report generated:"
    echo "  • Terminal: (see above)"
    echo "  • HTML: htmlcov/index.html"
    echo "  • XML: coverage.xml"
    echo ""
    echo "Open HTML report:"
    echo "  open htmlcov/index.html"
else
    echo ""
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    exit 1
fi
