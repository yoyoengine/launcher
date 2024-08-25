#!/usr/bin/env bash

echo "Uninstalling YoyoEngine Hub..."

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 
    exit 1
fi

# Define directories and files
bin_directory="/usr/local/bin"
icon_directory="/usr/share/icons/hicolor/512x512/apps"
desktop_directory="/usr/share/applications"
executable="$bin_directory/yoyoengine-hub"
icon="$icon_directory/yoyoengine-hub.png"
desktop_file="$desktop_directory/yoyoengine-hub.desktop"

# Remove the executable
if [[ -f "$executable" ]]; then
    rm "$executable"
    echo "Removed $executable"
else
    echo "$executable not found"
fi

# Remove the icon
if [[ -f "$icon" ]]; then
    rm "$icon"
    echo "Removed $icon"
else
    echo "$icon not found"
fi

# Remove the .desktop file
if [[ -f "$desktop_file" ]]; then
    rm "$desktop_file"
    echo "Removed $desktop_file"
else
    echo "$desktop_file not found"
fi

# Update the desktop database
update-desktop-database "$desktop_directory"

# Display a success message
echo "YoyoEngine Hub has been successfully uninstalled."