import redis
import board
import neopixel
import time

# Constants
PIXEL_PIN = board.D18
NUM_PIXELS = 22
STATUS_LIGHTS = 12
BAR_GRAPH_PIXELS = 10

# Create a NeoPixel object
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False)

# Connect to Redis
r = redis.StrictRedis(host='192.168.20.71', port=6379, db=0)

def set_status_light(index, color):
    """Set the color of a status light."""
    pixels[index] = color

def set_bar_graph(level):
    """Set the bar graph LEDs to a given level (0-10)."""
    if level < 3:
        color = (0, 0, 255)
    elif level < 8:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    for i in range(BAR_GRAPH_PIXELS):
        if i < level:
            pixels[STATUS_LIGHTS + i] = color
        else:
            pixels[STATUS_LIGHTS + i] = (0, 0, 0)

# Status to RGB mapping
status_to_rgb = {
    'NOMINAL': (0, 128, 0),
    'COLD': (0, 0, 128),
    'SCRAM': (128, 0, 0),
    'RUNAWAY': (128, 0, 0),
    'ON': (0, 128, 0),
    'OFF': (0, 0, 128),
    'FAULT': (128, 0, 0),
}

# Updated names of the status lights based on your given systems
status_light_names = [
    "Reactor", 
    "EnvironmentalSystems", 
    "LifeSupport", 
    "Comms", 
    "DefensiveSystems", 
    "PsychicDiffuser", 
    "Maglev", 
    "AccessControl", 
    "SpiritContainmentField",
    "Placeholder_10",
    "Placeholder_11",
    "Placeholder_12"
]

while True:
    # Update named status lights
    for i, light_name in enumerate(status_light_names):
        status_data = r.get(light_name)
        
        if status_data is None:
            color = (255, 0, 0)  # Default to red if the key is not found in Redis
        else:
            status_str = status_data.decode('utf-8')
            # Convert status string to its corresponding RGB value
            color = status_to_rgb.get(status_str, (255, 0, 0))  # Default to red if status is not recognized
        
        set_status_light(i, color)

    # Update bar graph
    level = int(r.get('bar_graph_level').decode('utf-8'))
    set_bar_graph(level)

    # Show changes
    pixels.show()

    # Polling interval
    time.sleep(0.5)