#!/bin/bash

echo "======================================================================="
echo "Welcome to the setup. This will set up the local virtual environment."
echo "It will then install all the required Python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

# Check if .venv folder exists
if [ -d ".venv" ]; then
    echo ".venv folder exists. Installing using pip..."
else
    echo "Creating .venv and installing using pip..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install required packages
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Please make sure it exists."
fi

# Initialise Database
python3 -m scripts.seed

# Deactivate virtual environment
deactivate

echo "----------------------------------------------------------------------"
echo "Setup complete!"
echo "======================================================================="

read -p "Press Enter to continue..."