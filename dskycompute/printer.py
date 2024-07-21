import os
import random
import redis
from PIL import Image
from escpos.printer import Usb

# Printer setup
# Replace Vendor id and Product id with the values for your printer
# You might find these using "lsusb" command in Linux
p = Usb(0x04b8, 0x0202, 0)

r = redis.Redis(host='192.168.20.71', port=6379, db=0)

# Image directory
image_dir = "ports"
char_dir = "chars"
note_dir = "notes"
sm_dir = "SM"

# DPI of the printer and new width in mm
dpi = 203
new_width_mm = 40

new_width_px = int((new_width_mm * dpi) / 25.4)

while True:
    try:
        # Check for chars
        for i in range(1, 11):
            char_key = f'char{i}'
            char_value = r.get(char_key)

            if char_value and char_value.decode('utf-8') == '1':
                # Clear flag in Redis
                r.set(char_key, '0')
                
                # Select random image
                image_name = random.choice(os.listdir(image_dir))
                image_path = os.path.join(image_dir, image_name)

                # Load and print image
                with Image.open(image_path) as img:
                	w_percent = new_width_px / float(img.size[0])
                	h_size = int((float(img.size[1]) * float(w_percent)))
                
                	# Resize and print the image
                	img = img.resize((new_width_px, h_size), Image.ANTIALIAS)
                	img.show()  # For testing, remove in production
                
                	p.image(img)
                	p.text("\n\n")

                # Print char details
                char_path = os.path.join(char_dir, f"char{i}.txt")
                with open(char_path, 'r') as f:
                    char_text = f.read()
                    p.text(char_text)
                    p.cut()

        # Check for notes
        for i in range(1, 11):
            note_key = f'note{i}'
            note_value = r.get(note_key)
            
            if note_value and note_value.decode('utf-8') == '1':
                # Clear flag in Redis
                r.set(note_key, '0')
                
                # Print note details
                note_path = os.path.join(note_dir, f"note{i}.txt")
                with open(note_path, 'r') as f:
                    note_text = f.read()
                    p.text(note_text)
                    p.cut()
                    
        # Check for notes
        for i in range(1, 11):
            sm_key = f'sm{i}'
            sm_value = r.get(sm_key)
            
            if sm_value and sm_value.decode('utf-8') == '1':
                # Clear flag in Redis
                r.set(sm_key, '0')
                
                # Print note details
                sm_path = os.path.join(sm_dir, f"sm{i}.txt")
                with open(sm_path, 'r') as f:
                    sm_text = f.read()
                    p.text(sm_text)
                    p.cut()

        # Sleep for a small duration
        #time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        #time.sleep(10)  # Sleep for longer on error to avoid rapid log spam