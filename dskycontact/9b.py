#!/usr/bin/env python3
import redis
import time

def main():
	# Connect to Redis
	r = redis.Redis(host='192.168.20.71', port=6379, db=0)
	# Set char1 to 1
	r.set('note3', '1')

    
if __name__ == '__main__':
    main()
