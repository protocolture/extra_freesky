import redis
import time

# Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

# Status indicators
status_indicators = {
    'Reactor': ['ON', 'COLD', 'SCRAM'],
    'Life Support': ['ON', 'OFF', 'FAULT'],
    'Air Pressure': ['ON', 'OFF', 'FAULT'],
    'Comms': ['ON', 'OFF', 'FAULT'],
    'Defensive Systems': ['ON', 'OFF', 'FAULT'],
    'Food Water and Waste': ['ON', 'OFF', 'FAULT'],
    'Maglev': ['ON', 'OFF', 'FAULT'],
    'Access Control': ['ON', 'OFF', 'FAULT'],
    'Containment': ['ON', 'OFF', 'FAULT'],
    'System Booted': ['YES', 'NO']
}

# Power requirement for each system
power_req = {
    'Life Support': 10,
    'Air Pressure': 5,
    'Comms': 15,
    'Defensive Systems': 15,
    'Maglev': 40,
    'Food Water and Waste': 5,
    'Access Control': 10,
    'Containment': 10
}

# Reset Redis with initial statuses
for status, states in status_indicators.items():
    r.set(status, states[1])  # sets all statuses to their 'OFF' equivalent

# Set initial power level
r.set('Power', '0')

class Program:
    def __init__(self, code, name, next_programs, req_status, req_power, text):
        self.code = code
        self.name = name
        self.next_programs = next_programs
        self.req_status = req_status
        self.req_power = req_power
        self.text = text

    def run(self):
        # Check that all required statuses are met
        for status, req in self.req_status.items():
            if r.get(status).decode() != req:
                print(f"Error: {status} is not {req}")
                return '1000'

        # Check that enough power is available
        if int(r.get('Power').decode()) < self.req_power:
            print(f"Error: Not enough power for {self.name}")
            return '1000'

        print(self.text)
        return input("Enter next program code: ")

# Create Program objects
programs = {
    '1000': Program('1000', 'ERROR', ['1001', '1101'], {}, 'System is in ERROR state'),
    '1001': Program('1001', 'BOOT', ['1101', '1000'], {'Reactor': 'ON'}, 'System booting up...'),
    '1101': Program('1101', 'Reactor Startup', ['1201', '1301', '1401', '1501', '1601', '1701', '1801', '1901', '1000'], {}, 'Starting up reactor...'),
    '1201': Program('1201', 'Life Support Startup', ['1301', '1000'], {'Power': '10', 'System Booted': 'YES', 'Air Pressure': 'ON'}, 'Starting up Life Support...'),
    '1301': Program('1301', 'Air Pressure Startup', ['1401', '1000'], {'Power': '5', 'System Booted': 'YES'}, 'Starting up Air Pressure...'),
    '1401': Program('1401', 'Comms Startup', ['1501', '1000'], {'Power': '15', 'System Booted': 'YES'}, 'Starting up Communications...'),
    '1501': Program('1501', 'Defensive Systems Startup', ['1601', '1000'], {'Power': '15', 'System Booted': 'YES'}, 'Starting up Defensive Systems...'),
    '1601': Program('1601', 'Maglev Startup', ['1701', '1000'], {'Power': '40', 'System Booted': 'YES'}, 'Starting up Maglev...'),
    '1701': Program('1701', 'Food Water and Waste Startup', ['1801', '1000'], {'Power': '5', 'System Booted': 'YES'}, 'Starting up Food Water and Waste Systems...'),
    '1801': Program('1801', 'Access Control Startup', ['1901', '1000'], {'Power': '10', 'System Booted': 'YES', 'Defensive Systems': 'ON'}, 'Starting up Access Control...'),
    '1901': Program('1901', 'Containment Startup', ['1000'], {'Power': '10', 'System Booted': 'YES', 'Defensive Systems': 'ON', 'Access Control': 'ON'}, 'Starting up Containment...')
}

# Start with ERROR state
current_program = '1000'

# Main loop
while True:
    try:
        # Update power status
        if r.get('Reactor').decode() == 'ON' and all(r.get(status).decode() == 'OFF' for status in status_indicators.keys() if status != 'Reactor'):
            r.set('Power', '80')
        else:
            power = 80
            for status, requirement in power_req.items():
                if r.get(status).decode() == 'ON':
                    power -= requirement
            r.set('Power', str(max(power, 0)))

        # Display current status and power
        print("Current Status:")
        for status, _ in status_indicators.items():
            print(f"{status}: {r.get(status).decode('utf-8')}")
        print(f"Power: {r.get('Power').decode('utf-8')}%")

        # Reactor scram if power reaches 0
        if r.get('Power').decode() == '0' and r.get('System Booted').decode() == 'YES':
            for status in status_indicators.keys():
                r.set(status, status_indicators[status][1])  # sets all statuses to their 'OFF' equivalent
            r.set('Reactor', 'SCRAM')
            current_program = '1000'
            print("Reactor SCRAM! Power reached 0. All systems have been reset.")

        # Run current program and get next program
        next_program = programs[current_program].run()
        while next_program not in programs[current_program].next_programs:
            print("Invalid program. Please enter a valid next program code.")
            next_program = input("Enter next program code: ")

        current_program = next_program
    except KeyboardInterrupt:
        break

