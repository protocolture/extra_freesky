#!/usr/bin/python
# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

Relay = [5, 6, 13, 16, 19, 20, 21, 26]

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(Relay[0], GPIO.OUT) # set a port/pin as an output   
GPIO.output(Relay[0], 1)       # set port/pin value to 1/GPIO.HIGH/True  
time.sleep(5)
GPIO.output(Relay[0], 0)       # set port/pin value to 0/GPIO.LOW/False  
printf("Smoke Complete")