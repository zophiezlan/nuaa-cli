#!/bin/bash
# NUAA WebUI Quick Start - Mac/Linux
# Double-click this file to start the WebUI (or run: bash START-WEBUI.sh)

clear

echo ""
echo "==================================================================="
echo ""
echo "          NUAA WebUI - One-Click Start (Mac/Linux)"
echo ""
echo "          Starting up... Please wait..."
echo ""
echo "==================================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3:"
    echo "  - Mac: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt-get install python3"
    echo "  - Fedora: sudo dnf install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Run the quick start script
python3 quick-start.py

# Keep window open if there's an error
if [ $? -ne 0 ]; then
    read -p "Press Enter to exit..."
fi
