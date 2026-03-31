#!/bin/bash
echo "============================================"
echo "  GAMIFY YOUR LIFE - INSTALLER"
echo "============================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found."
    echo "Install it with: sudo apt install python3"
    exit 1
fi

# Run the Python installer from the same directory as this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/install.py"
