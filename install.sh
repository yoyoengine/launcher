#!/usr/bin/env bash

echo "Installing YoyoEngine Hub..."

# Check dependencies
dependencies=("curl" "tar")
for dependency in "${dependencies[@]}"; do
    if ! command -v "$dependency" &> /dev/null; then
        echo "Error: $dependency is not installed."
        exit 1
    fi
done

# Download the file
download_url="$(curl -s https://api.github.com/repos/yoyoengine/launcher/releases/latest | grep -o "https://github.com/yoyoengine/launcher/releases/download/.*/yoyoengine-hub-linux-amd64.tar.gz")"
curl -LO "$download_url"

# Extract the contents of the tar.gz file
tar -xf yoyoengine-hub-linux-amd64.tar.gz -C /tmp/

# Move the ELF file to the bin directory
bin_directory="$(dirname "$(which curl)")"
mv /tmp/yoyoengine-hub/yoyoengine-hub "$bin_directory/"

# Set the executable permission for the ELF file
chmod +x "$bin_directory/yoyoengine-hub"

# Move the icon to the appropriate directory
icon_directory="$HOME/.local/share/icons/hicolor/512x512"
mkdir -p "$icon_directory"
curl -LO "https://github.com/yoyoengine/launcher/raw/6f036095e0da8bd1f178fcc3261b43d61f5b6d07/media/yoyoengine-hub.png"
mv yoyoengine-hub.png "$icon_directory/"

# Clean up the downloaded tar.gz file and extracted directory
rm yoyoengine-hub-linux-amd64.tar.gz
rm -rf /tmp/yoyoengine-hub/

# Create a .desktop file
desktop_file="$HOME/.local/share/applications/yoyoengine-hub.desktop"
cat > "$desktop_file" << EOL
[Desktop Entry]
Name=YoyoEngine Hub
Exec=$bin_directory/yoyoengine-hub
Icon=$icon_directory/yoyoengine-hub.png
Terminal=false
Type=Application
EOL
# Update the desktop database
update-desktop-database "$HOME/.local/share/applications"

# Display a success message
echo "YoyoEngine Hub has been successfully installed."