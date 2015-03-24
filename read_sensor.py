#!/usr/bin/env python2.7

# script to read GPIO with interrupts

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#GPIO 23 set as input, pulled up to avoid false detection.
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO 24 set as input, pulled down **optional**
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#define threaded callback function that will run in another thread
#when the events are detected
def event_detected(chanel):
	print "event detected on GPIO 23"

#when the falling edge is detected on port 23, no matter what happens in the
#program, the function event_detected will be run; bouncetime=100 sets a time
#of 100ms of a second when a second event will be ignored.
GPIO.add_event_detect(23, GPIO.FALLING, callback=event_detected, bouncetime=100)

try:
	print "Waiting for rising edge on GPIO 24"
	GPIO.wait_for_edge(24, GPIO.RISING)
	print "Rising edge detected on port 24"

except KeyboardInterrupt:
	GPIO.cleanup() #clean up GPIO on keyboard interrupt (CTRL+C)

GPIO.cleanup() #clean up the GPIO on normal exit


#for removing the event detection
#GPIO.remove_event_detect(port_number)
