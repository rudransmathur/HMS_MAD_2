#!/bin/bash

echo "======================================================================="
echo "Welcome to the setup. This will enable the local virtual environment."
echo "Then it will run the Python application."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

# Check if .venv folder exists
if [ -d "linux.venv" ]; then
    echo "Enabling virtual environment..."
else
    echo "No virtual environment found. Please run setup_env.sh first."
    exit 1
fi

# Activate virtual environment
source linux.venv/bin/activate

# Set environment variable
export ENV=development

# Run app
python app.py

# Deactivate virtual environment
deactivate

echo "----------------------------------------------------------------------"
echo "Done! Virtual environment deactivated."
echo "======================================================================="

read -p "Press Enter to continue..."