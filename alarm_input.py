#!/usr/bin/env python2.7

# script to read GPIO with interrupts

import RPi.GPIO as GPIO
import time

class alarm_input():
    #all alarm inputs will be configured by default as GPIO.IN
    self.GPIO_Type = GPIO.IN

    #alarm_input class constructor
    def __init__(self, IONumber, IOPull, IOEdge, IOTimeout):
	print "-==alarm_input constructor==-"
	print "GPIO %s"%IONumber
	print "GPIO PullUpDown %s"%IOPull
	print "GPIO Edge %s"%IOEdge
	print "GPIO Timeout %s"%IOTimeout

	GPIO.setmode(GPIO.BCM)

	# TODO checks on parameters if needed

	# CLASS MEMBERS
	self.GPIO_Number = IONumber		# 23
	self.GPIO_Pull = IOPull			# GPIO.PUD_UP
	self.GPIO_Edge = IOEdge			# GPIO.FALLING
	self.GPIO_Timeout = IOTimeout		# 100
	#GPIO set as input, pulled up to avoid false detection.
	GPIO.setup(self.GPIO_Number, self.GPIO_Type, pull_up_down=self.GPIO_Pull)

	#when the falling edge is detected on port 23, no matter what happens in the
	#program, the function event_detected will be run; bouncetime=100 sets a time
	#of 100ms of a second when a second event will be ignored.
	GPIO.add_event_detect(self.GPIO_Number, self.GPIO_Edge, callback=event_detected, bouncetime=self.GPIO_Timeout)


    #define threaded callback function that will run in another thread
    #when the events are detected
    def event_detected(self, channel):
	print "event detected on GPIO %s"%self.GPIO_Number

    #clean up the GPIO on normal exit
    def deinit()
	GPIO.cleanup()

	#The following lines kept as an example
	#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	##GPIO 24 set as input, pulled down **optional**
	#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	#when the falling edge is detected on port 23, no matter what happens in the
	#program, the function event_detected will be run; bouncetime=100 sets a time
	#of 100ms of a second when a second event will be ignored.
	#GPIO.add_event_detect(23, GPIO.FALLING, callback=event_detected, bouncetime=100)
	#try:
	#	print "Waiting for rising edge on GPIO 24"
	#	GPIO.wait_for_edge(24, GPIO.RISING)
	#	print "Rising edge detected on port 24"

	#except KeyboardInterrupt:
	#	GPIO.cleanup() #clean up GPIO on keyboard interrupt (CTRL+C)

	#for removing the event detection
	#GPIO.remove_event_detect(port_number)

