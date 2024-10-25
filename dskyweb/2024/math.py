import os
import time

# Clear the console for each update (cross-platform compatibility)
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Side temperatures initialized to -120 degrees
temperatures = {
    'A-B': -120,
    'B-C': -120,
    'C-A': -120
}

# Max and min temperatures
max_temp = 12000
min_temp = -120

# Heating, overlap, and cooling rates
heating_rate_full = 3  # Heating in full sun
heating_rate_overlap = 1  # Heating in overlap zone
cooling_rate = -6  # Cooling when not exposed to the sun

# Rotation speed (degrees per second, to achieve 360 degrees over 20 minutes)
rotation_speed = 360 / (20 * 60)  # 360 degrees over 1200 seconds (20 minutes)
rotation_angle = 0

# Function to update the temperature of the sides based on the current angle
def update_temperatures(angle):
    # Reset which sides are heating
    heating_sides = {'A-B': cooling_rate, 'B-C': cooling_rate, 'C-A': cooling_rate}

    # Determine which side is fully in the heating zone and which is in the overlap zone
    if 0 <= angle <= 110:
        heating_sides['A-B'] = heating_rate_full
        heating_sides['B-C'] = heating_rate_overlap
    elif 110 < angle <= 130:
        heating_sides['A-B'] = heating_rate_overlap
        heating_sides['B-C'] = heating_rate_full
    elif 130 < angle <= 230:
        heating_sides['B-C'] = heating_rate_full
        heating_sides['C-A'] = heating_rate_overlap
    elif 230 < angle <= 250:
        heating_sides['B-C'] = heating_rate_overlap
        heating_sides['C-A'] = heating_rate_full
    elif 250 < angle <= 350:
        heating_sides['C-A'] = heating_rate_full
        heating_sides['A-B'] = heating_rate_overlap
    else:
        heating_sides['C-A'] = heating_rate_overlap
        heating_sides['A-B'] = heating_rate_full

    # Update temperatures based on which sides are heating
    for side, rate in heating_sides.items():
        temperatures[side] = min(max(temperatures[side] + rate, min_temp), max_temp)

# Simulate the rotation of the triangle and update which sides are facing the sun
def simulate_rotation_over_20_minutes():
    global rotation_angle

    total_duration = 20 * 60  # 20 minutes in seconds
    start_time = time.time()

    while rotation_angle < 360:
        # Clear the console
        clear_console()

        # Get elapsed time and update rotation angle
        elapsed_time = time.time() - start_time
        rotation_angle = (elapsed_time * rotation_speed) % 360

        # Update temperatures based on the rotation angle
        update_temperatures(rotation_angle)

        # Output current state
        print(f"Rotation Angle: {rotation_angle:.2f}°")
        print(f"Temperatures: {temperatures}")
        print("---------------")

        # Sleep for 1 second before the next update
        time.sleep(1)

# Start the 20-minute simulation
simulate_rotation_over_20_minutes()
