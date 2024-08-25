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

# Move the ELF file to the bin directory
bin_directory="/usr/local/bin"
mkdir -p "$bin_directory"

# Extract the contents of the tar.gz file
tar -xf yoyoengine-hub-linux-amd64.tar.gz -C "$bin_directory"

# Set the executable permission for the ELF file
chmod +x "$bin_directory/yoyoengine-hub"

# Move the icon to the appropriate directory
icon_directory="/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$icon_directory"
curl https://raw.githubusercontent.com/yoyoengine/launcher/main/media/desktopicon.png > desktopicon.png
mv desktopicon.png "$icon_directory/yoyoengine-hub.png"

# Clean up the downloaded tar.gz file and extracted directory
rm yoyoengine-hub-linux-amd64.tar.gz

# Ensure the applications directory exists
desktop_directory="/usr/share/applications"
mkdir -p "$desktop_directory"

# Create a .desktop file
desktop_file="$desktop_directory/yoyoengine-hub.desktop"
cat > "$desktop_file" << EOL
[Desktop Entry]
Name=YoyoEngine Hub
Comment=The launcher and installation manager for yoyoengine.
Icon=$icon_directory/yoyoengine-hub.png
Exec=$bin_directory/yoyoengine-hub
Terminal=false
Type=Application
Categories=Utility;Development;
EOL
# Icon=/usr/share/icons/hicolor/128x128/apps/ark.png

# Ensure the .desktop file is executable
chmod +x "$desktop_file"

# Update the desktop database
update-desktop-database "$desktop_directory"

# Display a success message
echo "YoyoEngine Hub has been successfully installed."