#!/bin/bash

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run the script
uv run python ov_reports_list.py "$@"
