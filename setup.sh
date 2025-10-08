#!/bin/bash

echo "Setting up virtual environment..."

# Create virtual env if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv # TODO: Handle systems with python & python3
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source .venv/Scripts/activate

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "No requirements.txt found. Skipping package install."
fi