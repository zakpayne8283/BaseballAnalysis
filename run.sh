#!/bin/bash

# Notice: this file was heavily built with GPT

# Optional: Activate virtualenv
if [ -d ".venv" ]; then
    # Activate the virtual environment
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    else
        source .venv/Scripts/activate
    fi
else
    echo "⚠️  No .venv found. Did you run setup.sh?"
    exit 1
fi

# Pass all CLI args to Python entry point
python src/main.py "$@"