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
read -p "Enter the number corresponding to your choice: " choice

case $choice in
    1)
        env_var_value="DRelay"
        ;;
    2)
        env_var_value="DReader"
        ;;
    3)
        env_var_value="DPrinter"
        ;;
    4)
        env_var_value="DAudio"
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo "Setting environment variable EXTRA_FREESKY to $env_var_value"
echo "export EXTRA_FREESKY=\"$env_var_value\"" >> ~/.bashrc
echo "export EXTRA_FREESKY_PATH=\"$clone_dir\"" >> ~/.bashrc
source ~/.bashrc

# Step 3: Set the launch script to run at startup
echo "Setting up launch script to run at startup..."

# Create a systemd service file to run the launch script at startup
sudo bash -c 'cat << EOF > /etc/systemd/system/freesky.service
[Unit]
Description=Launch Freesky

[Service]
ExecStart='$launch_script_path'
Environment="EXTRA_FREESKY='$env_var_value'"
StandardOutput=journal
StandardError=journal
Restart=always
User='$USER'cat
WorkingDirectory='$HOME/repo'
[Install]
WantedBy=multi-user.target
EOF'

# Enable the systemd service
sudo systemctl enable freesky.service
echo "Installation complete. The extra_freesky script will run at startup."
