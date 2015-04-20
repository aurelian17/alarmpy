#!/usr/bin/env python

"""
alarm_input.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation for reading GPIO with interrupts
v 1.1 Added alarm_input class implementation
v 1.2 Added logging support for alarm_input class

----------------------------------------------------------------------------------------
"""


import RPi.GPIO as GPIO
import time					#for sleep
import logging					#for logging
import sys					#for logging

class alarm_input():

	# all alarm inputs will be configured by default as GPIO.IN
	GPIO_Type = GPIO.IN

	def __init__(self, IONumber, IOEdge, IOTimeout):
		"alarm_input class constructor"

		self.initDebugging()

		logging.debug("-==alarm_input constructor==-")
		logging.debug("-==alarm_input GPIO %s", IONumber)
		logging.debug("-==alarm_input GPIO Edge %s", IOEdge)
		logging.debug("-==alarm_input GPIO Timeout %s", IOTimeout)
		GPIO.setmode(GPIO.BCM)

		#TODO checks on parameters if needed

		# alarm_input class members
		self.GPIO_Number = IONumber		# 23
		self.GPIO_Edge = IOEdge			# GPIO.FALLING
		self.GPIO_Timeout = IOTimeout		# 100

		#GPIO set as input, without pull_up or pull_down configured resitors.
		GPIO.setup(int(self.GPIO_Number), self.GPIO_Type)

		#when the falling/rising edge is detected on port, no matter what happens in the
		#program, the function event_detected will be run; bouncetime sets a number of ms 
		#of a second when a second, when event will be ignored.
		GPIO.add_event_detect(int(self.GPIO_Number), int(self.GPIO_Edge), callback=self.event_detected, bouncetime=int(self.GPIO_Timeout))
		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def event_detected(self, channel):
		"define threaded callback function that will run in another thread when the events are detected"
		logging.debug("-==alarm_input event detected GPIO %s==-", channel)
		return


	def __del__(self):
		"clean up the GPIO on normal exit"
		logging.debug("-==alarm_input deinit()==-")
		GPIO.remove_event_detect(self.GPIO_Number)
		GPIO.cleanup()
		return

def main():
	"main function"
	print "-==alarm_input main()==-"
	# Initialize the alarm_input class
	ai1 = alarm_input(17, GPIO.RISING, 300)
	ai2 = alarm_input(21, GPIO.RISING, 300)
	ai3 = alarm_input(22, GPIO.RISING, 300)
	while True:
		time.sleep(1)
	return


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
