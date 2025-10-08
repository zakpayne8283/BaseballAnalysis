#!/bin/bash

# Notice: this file was heavily built with GPT

# Optional: Activate virtualenv
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
else
    echo "⚠️  No .venv found. Did you run setup.sh?"
    exit 1
fi

# Pass all CLI args to Python entry point
python src/main.py "$@"