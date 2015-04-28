#!/usr/bin/env python

"""
alarm_event.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation for singleton pattern

----------------------------------------------------------------------------------------
"""


import time					#for sleep
import logging					#for logging
import sys					#for logging


"""
  http://www.mindviewinc.com/Books/Python3Patterns/Index.php
"""
class Singleton:
	def __init__(self, klass):
		self.klass = klass
		self.instance = None
		return;

	def __call__(self, *args, **kwds):
		if self.instance == None:
			self.instance = self.klass(*args, **kwds)
		return self.instance

@Singleton
class alarm_event(object):
	INSTANCE = None

	def __init__(self):
		"alarm_event class constructor"

		#initialize the debugging system
		self.initDebugging()
		logging.debug("-==alarm_event constructor %s==-", self)

		if self.INSTANCE is not None:
			raise ValueError("An alarm_event instantiation already exists!")

		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def getEventInstance(cls):
		"Return the alarm_event single class instance"
		if cls.INSTANCE is None:
			cls.INSTANCE = alarm_event()
		return cls.INSTANCE

	def insertEvent(self, inputName, inputZone, inputGPIO):
		"Add a new alarm_event"
		logging.debug("-==alarm_event insert event: inputName: %s, inputZone: %s, inputGPIO: %s ==-", inputName, inputZone, inputGPIO)
		return

	def __del__(self):
		"clean up the alarm_event on normal exit"
		logging.debug("-==alarm_event destructor()==-")
		return

def main():
	"main function"
	print "-==alarm_event main()==-"
	# Initialize the alarm_input class
	ae1 = alarm_event().getEventInstance()
	ae2 = alarm_event().getEventInstance()
	ae3 = alarm_event().getEventInstance()
	ae1.insertEvent("GPIO_1", "Zone0", 17)
	ae3.insertEvent("GPIO_3", "Zone0", 22)
	ae2.insertEvent("GPIO_2", "Zone1", 21)

	ae1.insertEvent("GPIO_1", "Zone0", 17)
	ae2.insertEvent("GPIO_2", "Zone1", 21)
	ae3.insertEvent("GPIO_3", "Zone0", 22)

	ae2.insertEvent("GPIO_2", "Zone1", 21)
	ae3.insertEvent("GPIO_3", "Zone0", 22)
	ae1.insertEvent("GPIO_1", "Zone0", 17)

	while True:
		time.sleep(1)
	return


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
