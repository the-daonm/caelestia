#!/bin/bash

# Check if fish is installed
if ! command -v fish &> /dev/null; then
    echo "Error: fish shell is not installed. Please install fish to use this installer."
    exit 1
fi

# Run the fish installer
exec fish "$(dirname "$0")/install.fish" "$@"
