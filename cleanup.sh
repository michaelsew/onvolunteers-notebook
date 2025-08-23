#!/bin/bash
# This script cleans up the project directory.

# Deactivating the virtual environment must be done in the current shell.
# This script will remind the user to do so.

echo "Cleaning up log files..."
find . -name "*.log" -type f -delete

echo "Cleaning up screenshot files..."
find . -name "*.png" -type f -delete
find . -name "*.jpeg" -type f -delete
find . -name "*.jpg" -type f -delete

echo "Cleanup complete."
echo "To deactivate the virtual environment, please run the following command:"
echo "deactivate"
