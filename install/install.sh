#!/bin/bash
repo_url="https://github.com/protocolture/extra_freesky"
clone_dir="/opt/dsky"
launch_script_path="/opt/dsky/launch/launch_script.sh"



# Step 1: Pull the GitHub repository
#Check dir exists. 
if [ ! -d "$clone_dir" ]; then
    echo "Directory $clone_dir does not exist. Creating it..."
    mkdir -p "$clone_dir"
else
    echo "Directory $clone_dir already exists. Removing."
	rm -d -r "$clone_dir"
	mkdir -p "$clone_dir"
fi

echo "Cloning the repository into $clone_dir..."
git clone $repo_url $clone_dir

chmod +x $launch_script_path
sudo touch /var/log/dsky_launch.log
sudo chmod 664 /var/log/dsky_launch.log


# Erroor Checking
if [ $? -ne 0 ]; then
    echo "Error: Failed to clone repository. Please check the URL and your network connection. Exiting."
    exit 1
fi

# Step 2: Set the environment variable with options
echo "Select the mode for Extra_Freesky:"
echo "1) Relay"
echo "2) Reader"
echo "3) Printer"
echo "4) Audio"
read -p "Enter Mode: " choice

case $choice in
    1)
        FREESKY_MODE="DRelay"
        ;;
    2)
        FREESKY_MODE="DReader"
        ;;
    3)
        FREESKY_MODE="DPrinter"
        ;;
    4)
        FREESKY_MODE="DAudio"
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

# Ensure /etc/dsky directory exists
if [ ! -d /etc/dsky ]; then
    mkdir -p /etc/dsky
    echo "Created /etc/dsky directory."
fi

# Create the /etc/dsky/dsky.conf configuration file with the selected mode
sudo bash -c 'cat <<EOF > /etc/dsky/dsky.conf
# /etc/dsky/dsky.conf
# Configuration for Freesky

# Mode
FREESKY_MODE='$FREESKY_MODE'

# Directory for Freesky
FREESKY_DIR=/opt/dsky/freesky
EOF'

echo "Configuration file /etc/dsky/dsky.conf "

# Step 3: Set the launch script to run at startup
echo "Setting launch script to run at startup..."

# Create a systemd service file to run the launch script at startup
sudo bash -c 'cat << EOF > /etc/systemd/system/freesky.service
[Unit]
Description=Launch Freesky

[Service]
ExecStart='$launch_script_path'
StandardOutput=journal
StandardError=journal
Restart=always
WorkingDirectory='$HOME/repo'
[Install]
WantedBy=multi-user.target
EOF'

# Enable the systemd service
sudo systemctl enable freesky.service
echo "Installation complete. The extra_freesky script will run at startup."
