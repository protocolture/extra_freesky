import redis
import RPi.GPIO as GPIO
import time

# Set up the GPIO
GPIO.setmode(GPIO.BCM)  
GPIO.setup(5, GPIO.OUT, initial=GPIO.HIGH)  # GOSMOKE
GPIO.setup([6, 13, 16, 19], GPIO.OUT, initial=GPIO.HIGH)  # SCs

# Connect to Redis
r = redis.Redis(host='192.168.20.71', port=6379, db=0)

try:
    while True:
        # Fetch data from Redis
        go_smoke = r.get('GOSMOKE')
        smoke_seconds = r.get('Smokeseconds')
        sc1 = r.get('SC1')
        sc_seconds = r.get('SCseconds')
        
        # Decode and type convert fetched data
        go_smoke = bool(int(go_smoke.decode('utf-8'))) if go_smoke else False
        smoke_seconds = int(smoke_seconds.decode('utf-8')) if smoke_seconds else 0
        sc1 = bool(int(sc1.decode('utf-8'))) if sc1 else False
        sc_seconds = int(sc_seconds.decode('utf-8')) if sc_seconds else 0
        
        # Determine max duration to prevent issues if both commands arrive at once
        max_duration = max(smoke_seconds, sc_seconds)
        
        # Operate GOSMOKE and SCs based on conditions
        if go_smoke or sc1:
            if go_smoke:
                GPIO.output(5, GPIO.LOW)  # Activate GOSMOKE
            if sc1:
                GPIO.output([6, 13, 16, 19], GPIO.LOW)  # Activate SCs
                
            time.sleep(max_duration)  # Hold for the longer of the durations
            
            # Deactivate relays after holding
            GPIO.output([5, 6, 13, 16, 19], GPIO.HIGH)
            
            # Reset GOSMOKE and SC1 in Redis
            r.set('GOSMOKE', '0')
            r.set('SC1', '0')
            
        else:
            print("Waiting for command...")
            time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    GPIO.cleanup()