#!/usr/bin/env bash

echo "Uninstalling YoyoEngine Hub..."

# Define paths
bin_directory="$(dirname "$(which curl)")"
icon_directory="$HOME/.local/share/icons/hicolor/512x512"
desktop_file="$HOME/.local/share/applications/yoyoengine-hub.desktop"

# Remove the executable file
if [ -f "$bin_directory/yoyoengine-hub" ]; then
    rm "$bin_directory/yoyoengine-hub"
    echo "Removed executable from $bin_directory"
else
    echo "Executable not found in $bin_directory"
fi

# Remove the icon file
if [ -f "$icon_directory/yoyoengine-hub.png" ]; then
    rm "$icon_directory/yoyoengine-hub.png"
    echo "Removed icon from $icon_directory"
else
    echo "Icon not found in $icon_directory"
fi

# Remove the .desktop file
if [ -f "$desktop_file" ]; then
    rm "$desktop_file"
    echo "Removed .desktop file from $desktop_file"
else
    echo ".desktop file not found in $desktop_file"
fi

# Update the desktop database
update-desktop-database "$HOME/.local/share/applications"

# Display a success message
echo "YoyoEngine Hub has been successfully uninstalled."