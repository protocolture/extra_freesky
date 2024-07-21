import redis

# Configuration for Redis
redis_host = '192.168.20.71'
redis_port = 6379
redis_password = ''  # If your Redis server requires a password, set it here.

# Known keys - add all keys that you want to track
known_keys = [
    'RED', 'BLUE', 'YELLOW', 'GOSMOKE', 'smokeseconds',
    'POWERUP', 'SCRAM', 'alarm', 'RANT', 'WANK', 'SC1' , 'scseconds' ,
    # Add any other keys you want to track here
]

# Initialize the Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

def get_value(key):
    value = redis_client.get(key)
    print(f"The value of {key} is: {value}")
    return value

def set_value(key, value):
    redis_client.set(key, value)
    print(f"Set {key} to {value}.")

def print_all_values():
    print("\nCurrent values of known keys:")
    for key in known_keys:
        print(f"{key}: {redis_client.get(key)}")
    print()

def main():
    print_all_values()  # Print all known variables initially
    
    while True:
        print("\nAvailable commands:")
        print("get [key] - Retrieves the value of a key")
        print("set [key] [value] - Sets the value of a key")
        print("refresh - Refreshes and displays all known variables")
        print("exit - Exits the script\n")
        
        command = input("Enter command: ").strip().split()
        
        if len(command) == 0:
            continue
        
        if command[0] == 'exit':
            break

        if command[0] == 'refresh':
            print_all_values()
        elif command[0] == 'get' and len(command) == 2:
            get_value(command[1])
        elif command[0] == 'set' and len(command) == 3:
            set_value(command[1], command[2])
        else:
            print("Unknown command or wrong number of arguments.")

if __name__ == '__main__':
    main()