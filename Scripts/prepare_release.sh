#!/usr/bin/env bash
set -e

# ---------------------
# Prepare Release Files Script
# Collects all built CLI binaries into a single release-files directory
# ---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default artifacts directory (can be overridden by first argument)
ARTIFACTS_DIR="${1:-$PROJECT_ROOT/artifacts}"
RELEASE_DIR="${2:-$PROJECT_ROOT/release-files}"

echo "================================================"
echo "  Preparing CLI Release Files"
echo "================================================"
echo ""
echo "Artifacts Dir: $ARTIFACTS_DIR"
echo "Release Dir:   $RELEASE_DIR"
echo ""

# Create release directory
mkdir -p "$RELEASE_DIR"

# Find and copy all CLI binary artifacts from dist directories
echo "Collecting CLI binary artifacts..."

# Copy all CLI binaries from dist folders in artifacts
find "$ARTIFACTS_DIR" -type f \( -name "8085-simulator*" -o -name "8085-simulator-*" \) -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true

# Also search in dist subdirectories
find "$ARTIFACTS_DIR" -path "*/dist/*" -type f \( -name "8085-simulator*" -o -name "8085-simulator-*" \) -exec cp {} "$RELEASE_DIR/" \; 2>/dev/null || true

echo ""
echo "================================================"
echo "  Release Files"
echo "================================================"
echo ""
ls -lh "$RELEASE_DIR/"

FILE_COUNT=$(find "$RELEASE_DIR" -type f | wc -l)
echo ""
echo "Total files: $FILE_COUNT"
echo ""
