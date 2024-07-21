import redis
import time
import sys

# Redis connection
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

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
    'SystemBooted': ['YES', 'NO']
}

# Reset Redis with initial statuses
for status, states in status_indicators.items():
    redis_conn.set(status, states[1])  # sets all statuses to their 'OFF' equivalent

# Set initial power level
redis_conn.set('Power', '0')

class Program:
    def __init__(self, code, name, next_programs, req_status, text):
        self.code = code
        self.name = name
        self.next_programs = next_programs
        self.req_status = req_status
        self.text = text
        self.redis = redis_conn

    def run(self):
        # Check that all required statuses are met
        for status, req in self.req_status.items():
            if self.redis.get(status).decode('utf-8') != req:
                print(f"Error: {status} is not {req}")
                return '1000'
        print(self.text)
        next_program = self.get_next_program_code()
        return next_program

    def get_next_program_code(self):
        print("Current Status:")
        for status, _ in status_indicators.items():
            print(f"{status}: {self.redis.get(status).decode('utf-8')}")
        print(f"Power: {self.redis.get('Power').decode('utf-8')}%")
        next_program = input("Enter next program code: ")
        while next_program not in self.next_programs:
            print("Invalid program. Please enter a valid next program code.")
            next_program = input("Enter next program code: ")
        return next_program

class Error(Program):
    def __init__(self):
        super().__init__('1000', 'ERROR', ['1001', '1101', '1000'], {}, "System is in ERROR state")

class Boot(Program):
    def __init__(self):
        super().__init__('1001', 'BOOT', ['1101', '1000'], {'Reactor': 'ON', 'SystemBooted': 'NO'}, "System booting up...")

    def run(self):
        if super().run() == '1000':
            return '1000'
        print("System booting progress:")
        for i in range(10):
            time.sleep(1)
            print("#", end='', flush=True)
        print("\nSystem booted successfully!")
        self.redis.set('SystemBooted', 'YES')
        next_program = self.get_next_program_code()
        return next_program

class ReactorStartup(Program):
    def __init__(self):
        super().__init__('1101', 'Reactor Startup', ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010', '1000'], {}, "Starting up reactor...")

    def run(self):
        reactor_status = self.redis.get('Reactor').decode('utf-8')
        if reactor_status == 'COLD':
            print("Reactor is heating up. Progress:")
            for i in range(120):
                time.sleep(0.5)
                print("#", end='', flush=True)
            print("\nReactor has been heated and is now ON.")
            self.redis.set('Reactor', 'ON')
            self.redis.set('Power', 100)
        elif reactor_status == 'SCRAM':
            print("Reactor is in SCRAM state. Trying to reset...")
            for i in range(120):
                time.sleep(0.5)
                print("#", end='', flush=True)
            print("\nReactor has been restarted from SCRAM state.")
            self.redis.set('Reactor', 'ON')
            self.redis.set('Power', 100)
        else:
            print("Reactor is already ON.")
        next_program = self.get_next_program_code()
        return next_program

# Remaining Program classes ...

# Create Program objects
programs = {
    '1000': Error(),
    '1001': Boot(),
    '1101': ReactorStartup(),
    # ... rest of the programs
}

# Start with ERROR state
current_program_code = '1000'

while True:
    current_program = programs[current_program_code]
    current_program_code = current_program.run()

