#!/bin/bash
echo "Pulling the latest code from the GitHub repository..."
git -C /opt/dsky pull
CONFIG_FILE="/etc/dsky/dsky.conf"

#!/bin/bash

# Load configuration from /etc/dsky/dsky.conf

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
    echo "Configuration loaded from $CONFIG_FILE"
else
    echo "Configuration file $CONFIG_FILE not found. Exiting."
    exit 1
fi

# Map environment variables to specific scripts
echo $FREESKY_MODE
case $FREESKY_MODE in
    DRelay)
        script_to_run="/opt/dsky/dskyrelay/free-sky-relay-loop.py"
        ;;
    DReader)
        script_to_run="/opt/dsky//dskycontact/main.py"
        ;;
    DPrinter)
        script_to_run="/opt/dsky//dskycompute/admin.py"
        ;;
    DAudio)
        script_to_run="/opt/dsky//dskybrain/brain.py"
        ;;
    *)
        echo "Unsupported mode, Exiting"
        exit 1
        ;;
esac

# Check if the script exists and run it
if [ -f "$script_to_run" ]; then
    python3 "$script_to_run"
else
    echo "Script $script_to_run not found. Exiting."
    exit 1
fi
