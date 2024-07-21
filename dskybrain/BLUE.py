import redis

# Connect to Redis
r = redis.Redis(host='192.168.20.71', port=6379, db=0)

def check_and_set_values():
    # Check if RED, BLUE, and YELLOW are all set to "1"
    if r.get('RED') == b'1' and r.get('BLUE') == b'1' and r.get('YELLOW') == b'1':
        # Set the other values if the conditions are met
        r.set('GOSMOKE', '1')
        r.set('smokeseconds', '12')
        r.set('POWERUP', '1')
        # Reset RED, BLUE, and YELLOW to "0"
        r.set('RED', '0')
        r.set('BLUE', '0')
        r.set('YELLOW', '0')
        print("Values set and RED, BLUE, YELLOW reset!")
    else:
        print("RED, BLUE, and YELLOW are not all set to '1'")

check_and_set_values()