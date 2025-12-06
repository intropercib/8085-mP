#!/bin/bash
set -e

echo "=== Setting up 8085-mP Dev Environment ==="

# Determine script/project paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo ">>> Setting up Python environment..."

# Use project-root .venv and requirements.txt (requirements moved to project root)
VENV_DIR="$PROJECT_ROOT/.venv"

# Remove old/broken venv if it exists
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing $VENV_DIR (may be from different Python version)..."
    rm -rf "$VENV_DIR"
fi

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
python3 -m pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"
deactivate

# Node setup
echo ">>> Setting up Node.js environment..."
cd "$PROJECT_ROOT" || { echo "Failed to cd to $PROJECT_ROOT"; exit 1; }
npm ci

echo "=== Setup Complete ==="
echo "Python venv: .venv (activate with: source .venv/bin/activate)"
echo "To run: python -m Server & npm run tauri dev"
