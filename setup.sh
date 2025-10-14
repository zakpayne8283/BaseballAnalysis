#!/bin/bash

# TODO: Download the retrosheet files
# curl https://www.retrosheet.org/downloads/plays/2024plays.zip ? 
# extract it too?
# drop it in /data/

echo "Setting up virtual environment..."

# Create virtual env if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv # TODO: Handle systems with python & python3
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    source .venv/Scripts/activate
fi

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "No requirements.txt found. Skipping package install."
fi