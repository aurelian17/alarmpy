#!/usr/bin/env python

"""
alarm_input.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation for reading GPIO with interrupts
v 1.1 Added alarm_input class implementation
v 1.2 Added logging support for alarm_input class
v 1.3 Added alarm_input GPIO_Name field for compatibility with alarm_zone class
v 1.4 Added link with alarm_event singleton class in order to log all alarm events

----------------------------------------------------------------------------------------
"""


import RPi.GPIO as GPIO
import time					#for sleep
import logging					#for logging
import sys					#for logging

import alarm_event

class alarm_input():

	# all alarm inputs will be configured by default as GPIO.IN
	GPIO_Type = GPIO.IN

	def __init__(self, IONumber, IOEdge, IOTimeout, IOName):
		"alarm_input class constructor"

		self.initDebugging()

		logging.debug("-==alarm_input constructor==-")
		logging.debug("-==alarm_input GPIO %s==-", IONumber)
		logging.debug("-==alarm_input GPIO Edge %s==-", IOEdge)
		logging.debug("-==alarm_input GPIO Timeout %s==-", IOTimeout)
		logging.debug("-==alarm_input GPIO Name %s==-", IOName)
		GPIO.setmode(GPIO.BCM)

		#TODO checks on parameters if needed

		# alarm_input class members
		self.GPIO_Name = IOName
		self.GPIO_Number = IONumber
		self.GPIO_Edge = IOEdge
		self.GPIO_Timeout = IOTimeout
		self.GPIO_Zone = ''

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

	def setZone(self, zoneName):
		"set zone for alarm_input"
		logging.debug("-==alarm_input setZone (%s) ==-", zoneName)
		self.GPIO_Zone = zoneName
		return

	def event_detected(self, channel):
		"define threaded callback function that will run in another thread when the events are detected"
		logging.debug("-==alarm_input event detected  Zone %s : GPIO %s - %s==-", self.GPIO_Zone, self.GPIO_Name, channel)
		alarm_event.alarm_event().getEventInstance().insertEvent(self.GPIO_Name, self.GPIO_Zone, channel)
		return

	def __del__(self):
		"clean up the GPIO on normal exit"
		logging.debug("-==alarm_input destructor()==-")
		GPIO.remove_event_detect(self.GPIO_Number)
		GPIO.cleanup()
		return

def main():
	"main function"
	print "-==alarm_input main()==-"
	# Initialize the alarm_input class
	ai1 = alarm_input(17, GPIO.RISING, 300, "Contact 1")
	ai2 = alarm_input(21, GPIO.RISING, 300, "Contact 2")
	ai3 = alarm_input(22, GPIO.RISING, 300, "PIR 1")
	while True:
		time.sleep(1)
	return


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
