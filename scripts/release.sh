#!/bin/bash
# Orbit Release Script
# This script automates the release process for Orbit

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "src/orbit" ]; then
    print_error "Must be run from project root directory"
    exit 1
fi

# Get version from pyproject.toml
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
print_header "Orbit Release v$VERSION"

# Step 1: Check git status
print_header "Step 1: Checking Git Status"
if [ -n "$(git status --porcelain)" ]; then
    print_error "Working directory is not clean"
    git status
    exit 1
fi
print_success "Working directory is clean"

# Step 2: Run tests
print_header "Step 2: Running Tests"
if command -v poetry &> /dev/null; then
    poetry install --with dev
    poetry run pytest tests/ -v
    print_success "All tests passed"
else
    print_warning "Poetry not found, skipping tests"
fi

# Step 3: Build package
print_header "Step 3: Building Package"
if command -v poetry &> /dev/null; then
    poetry build
    print_success "Package built successfully"
else
    print_error "Poetry is required to build the package"
    exit 1
fi

# Step 4: Check distribution files
print_header "Step 4: Checking Distribution Files"
DIST_DIR="dist"
if [ ! -d "$DIST_DIR" ]; then
    print_error "dist directory not found"
    exit 1
fi

FILE_COUNT=$(ls -1 "$DIST_DIR" | wc -l)
if [ "$FILE_COUNT" -lt 2 ]; then
    print_error "Expected at least 2 files in dist/, found $FILE_COUNT"
    exit 1
fi
print_success "Found $FILE_COUNT distribution file(s)"

# List files
ls -lh "$DIST_DIR"

# Step 5: Create git tag
print_header "Step 5: Creating Git Tag"
TAG_NAME="v$VERSION"

if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    print_warning "Tag $TAG_NAME already exists"
    read -p "Delete existing tag and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "$TAG_NAME"
        git push --delete origin "$TAG_NAME" 2>/dev/null || true
        print_success "Deleted existing tag"
    else
        print_error "Aborting release"
        exit 1
    fi
fi

git tag -a "$TAG_NAME" -m "Release $TAG_NAME"
print_success "Created tag $TAG_NAME"

# Step 6: Upload to PyPI (with confirmation)
print_header "Step 6: Upload to PyPI"
echo "Files to be uploaded:"
ls -1 "$DIST_DIR"

echo ""
read -p "Upload to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    poetry publish
    print_success "Published to PyPI"
else
    print_warning "Skipped PyPI upload"
fi

# Step 7: Push tag to GitHub
print_header "Step 7: Push Tag to GitHub"
read -p "Push tag $TAG_NAME to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin "$TAG_NAME"
    print_success "Pushed tag to GitHub"
else
    print_warning "Skipped pushing tag"
fi

# Step 8: Create GitHub release (manual step)
print_header "Step 8: Create GitHub Release"
echo "Please manually create a GitHub release at:"
echo "https://github.com/xiaoxiath/orbit/releases/new?tag=$TAG_NAME"
echo ""
echo "Release notes from CHANGELOG.md:"
grep -A 20 "## \[$VERSION\]" CHANGELOG.md || echo "No changelog entry found"

# Final summary
print_header "Release Summary"
print_success "Version: $VERSION"
print_success "Tag: $TAG_NAME"
print_success "Files: $FILE_COUNT"

echo ""
echo -e "${GREEN}Release v$VERSION is ready!${NC}"
echo ""
echo "Next steps:"
echo "1. Create GitHub release with release notes"
echo "2. Verify PyPI package at: https://pypi.org/project/orbit-macos/"
echo "3. Test installation: pip install orbit-macos==$VERSION"
echo "4. Announce the release"
echo ""
