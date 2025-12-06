#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Project root is the parent of the `Scripts` folder
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root so relative paths (like `requirements.txt`)
# resolve correctly even when the script is run from elsewhere.
cd "$PROJECT_ROOT" || { echo "Failed to cd to project root: $PROJECT_ROOT"; exit 1; }

python3 -m venv .venv
# shellcheck source=/dev/null
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt