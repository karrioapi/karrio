#!/usr/bin/env bash

# Get the absolute path to the Karrio root directory
KARRIO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "This script requires sudo privileges to create a symlink in /usr/local/bin"
    echo "Please run with sudo: sudo $0"
    exit 1
fi

# Create symlink to the kcli script in /usr/local/bin
ln -sf "${KARRIO_ROOT}/bin/kcli" /usr/local/bin/kcli
chmod +x "${KARRIO_ROOT}/bin/kcli"

# Make sure the modules/cli/__main__.py is executable
chmod +x "${KARRIO_ROOT}/modules/cli/__main__.py"

echo "✅ kcli command has been set up globally."
echo "You can now run 'kcli' from anywhere on your system."
echo "Try running: kcli --help" 