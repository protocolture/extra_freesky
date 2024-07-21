import RPi.GPIO as GPIO
import subprocess
import os
import time

from pn532 import *

def execute_script(hex_value):
    """Executes the Python script corresponding to the hex value."""
    script_name = f"{hex_value}.py"
    if os.path.exists(script_name):  # Check if the script exists
        try:
            subprocess.run(["python3", script_name])
            time.sleep(2)
            print(f"Ready")
        except Exception as e:
            print(f"Failed to execute {script_name}. Error: {e}")
    else:
        print(f"Script {script_name} not found.")

if __name__ == '__main__':
    try:
        pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            
            # Try again if no card is available.
            if uid is None:
                continue
            
            print('Found card with UID:', [hex(i) for i in uid])
            
            # Extract hex(0) and attempt to execute the corresponding script
            hex_value = hex(uid[0])[2:]  # Strip off the "0x" prefix
            execute_script(hex_value)

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
