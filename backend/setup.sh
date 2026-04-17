#!/bin/bash

echo "======================================================================="
echo "Welcome to the setup. This will set up the local virtual environment."
echo "It will then install all the required Python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"

# Check if linux.venv folder exists
if [ -d "linux.venv" ]; then
    echo "linux.venv folder exists. Installing using pip..."
else
    echo "Creating linux.venv and installing using pip..."
    python3 -m venv linux.venv
fi

# Activate virtual environment
source linux.venv/bin/activate

# Install required packages
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Please make sure it exists."
fi

mkdir -p /path/to/your/directory

# Initialise Database
python3 -m scripts.seed

# Deactivate virtual environment
deactivate

echo "----------------------------------------------------------------------"
echo "Setup complete!"
echo "======================================================================="

read -p "Press Enter to continue..."
