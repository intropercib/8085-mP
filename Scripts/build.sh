#!/usr/bin/env bash
set -e

# ---------------------
#  CONFIG
# ---------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLI_DIR="$PROJECT_ROOT/CLI"
BACKEND_DIR="$PROJECT_ROOT/Backend"
RELEASE_DIR="$PROJECT_ROOT/release"

ENTRY_POINT="CLI"
OUTPUT_DIR="dist"

echo "================================================"
echo "  8085 Microprocessor Simulator - CLI Build Script"
echo "================================================"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "CLI Dir:      $CLI_DIR"
echo "Backend Dir:  $BACKEND_DIR"
echo "Release Dir:  $RELEASE_DIR"
echo ""

# Setup a project-root virtual environment so build dependencies
# (like Nuitka) can be installed and used reproducibly.
VENV_DIR="$PROJECT_ROOT/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "🛠 Creating virtualenv at $VENV_DIR"
    python3 -m venv "$VENV_DIR" || { echo "❌ Failed to create venv at $VENV_DIR"; exit 1; }
else
    echo "ℹ️  Using existing virtualenv at $VENV_DIR"
fi
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo "📦 Installing Python requirements from $PROJECT_ROOT/requirements.txt"
    python -m pip install -r "$PROJECT_ROOT/requirements.txt"
else
    echo "⚠️  No requirements.txt found at $PROJECT_ROOT/requirements.txt — continuing"
fi

# Clean old builds
echo "🧹 Cleaning old builds..."
rm -rf "$PROJECT_ROOT/$OUTPUT_DIR" "$PROJECT_ROOT/build" "$PROJECT_ROOT"/*.dist "$PROJECT_ROOT"/*.build 2> /dev/null || true

echo "🔨 Building CLI using Nuitka (onefile)..."
echo ""

cd "$PROJECT_ROOT"

# Check if Nuitka is installed (use venv python)
if ! python -m nuitka --version > /dev/null 2>&1; then
    echo "❌ Error: Nuitka is not installed in the active Python environment."
    echo "   Install it with: python -m pip install nuitka"
    exit 1
fi

# Check for required system dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v patchelf &> /dev/null; then
        echo "❌ Error: patchelf is not installed."
        echo "   Install it with: sudo apt-get install patchelf"
        exit 1
    fi
fi

# Build with Nuitka (uses active Python from venv)
python -m nuitka \
  --standalone \
  --onefile \
  --follow-imports \
  --enable-plugin=no-qt \
  --python-flag=-m \
  --assume-yes-for-downloads \
  --include-data-files=Backend/M8085/commands_property.yml=Backend/M8085/commands_property.yml \
  --include-data-files=Backend/M8085/docs.yml=Backend/M8085/docs.yml \
  --output-dir=${OUTPUT_DIR} \
  $ENTRY_POINT

echo ""
echo "🎉 Nuitka build complete!"
echo ""

# Create release directory
mkdir -p "$RELEASE_DIR"

# Copy the CLI binary to release directory
echo "📦 Preparing CLI binary for release..."

# Detect OS and set correct binary name
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    SOURCE_BINARY="$PROJECT_ROOT/$OUTPUT_DIR/CLI.exe"
    DEST_BINARY="$RELEASE_DIR/8085-simulator.exe"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SOURCE_BINARY="$PROJECT_ROOT/$OUTPUT_DIR/CLI.bin"
    DEST_BINARY="$RELEASE_DIR/8085-simulator-macos"
else
    SOURCE_BINARY="$PROJECT_ROOT/$OUTPUT_DIR/CLI.bin"
    DEST_BINARY="$RELEASE_DIR/8085-simulator"
fi

# Check if source binary exists
if [ ! -f "$SOURCE_BINARY" ]; then
    echo "❌ Error: Binary not found at $SOURCE_BINARY"
    echo "   Looking for alternatives..."
    ls -la "$BACKEND_DIR/$OUTPUT_DIR/" 2>/dev/null || echo "   Output directory does not exist"
    exit 1
fi

# Copy and set permissions
cp "$SOURCE_BINARY" "$DEST_BINARY"
chmod +x "$DEST_BINARY"

echo "✅ CLI binary created: $DEST_BINARY"

# Verify the binary
if [ -x "$DEST_BINARY" ]; then
    echo "✓ CLI binary is executable"
    # Show binary size
    SIZE=$(du -h "$DEST_BINARY" | cut -f1)
    echo "✓ Binary size: $SIZE"
else
    echo "⚠️  Warning: CLI binary may not be executable"
fi

echo ""
echo "================================================"
echo "  Build Summary"
echo "================================================"
echo ""
echo "CLI binary:      $DEST_BINARY"
echo "Release dir:     $RELEASE_DIR"
echo ""
echo "🚀 Usage:"
echo "   Run the CLI: $DEST_BINARY"
echo ""
echo "📝 For development:"
echo "   python -m CLI"
echo ""