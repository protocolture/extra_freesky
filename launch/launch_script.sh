#!/bin/bash
# Step 1: Pull the latest code from the GitHub repository
echo "Pulling the latest code from the GitHub repository..."
git -C /opt/dsky pull

# Step 2: Launch a script based on the environment variable
echo "Launching Freesky..."

# Map environment variables to specific scripts
echo $EXTRA_FREESKY
case $EXTRA_FREESKY in
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
        echo "Unsupported mode: $EXTRA_FREESKY. Exiting."
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
