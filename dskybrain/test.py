import asyncio
from kasa import SmartStrip

async def kasa_control():
    # Initialize the SmartStrip at IP 192.168.20.148
    strip1 = SmartStrip("192.168.20.148")
    await strip1.update()

    # Turn on plug at index 1
    await strip1.children[1].turn_on()
    await asyncio.sleep(2)

    # Turn on other plugs
    await strip1.children[0].turn_on()
    
    strip2 = SmartStrip("192.168.20.63")
    await strip2.update()
    await strip2.children[0].turn_on()

    strip3 = SmartStrip("192.168.20.64")
    await strip3.update()
    await strip3.children[0].turn_on()
    await strip3.children[1].turn_on()
    await strip3.children[2].turn_on()
    
    await asyncio.sleep(2)

    # Turn off plug at index 1 of 192.168.20.148
    await strip1.children[1].turn_off()

# Run the asynchronous function
asyncio.run(kasa_control())
