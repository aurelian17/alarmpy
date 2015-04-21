#!/usr/bin/env python

"""
alarm_zone.py
--------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only primary implementation for alarm zones

--------------------------------------------------------------------------------
"""

import logging						#for logging
import sys						#for logging
import time						#for sleep


class alarm_zone():
	# alarm_zone class constants

	def __init__(self, Name, NumberInputs):
		"alarm_zone class constructor"
		self.initDebugging()
		logging.debug("-==alarm_zone constructor (%s %s)==-", Name, NumberInputs)
		self.name = Name
		self.inputs = NumberInputs
		self.zoneInputsGPIOs = []
		self.zoneInputsNames = []
		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def addAlarmInput(self, AlarmInputName, AlarmInputGPIO):
		"alarm_zone method used for adding new inputs to zone"
		logging.debug("-==alarm_zone addAlarmInput(Name %s, GPIO %s)==-", AlarmInputName, AlarmInputGPIO)
		self.zoneInputsGPIOs.append(int(AlarmInputGPIO))
		self.zoneInputsNames.append(str(AlarmInputName))
		logging.debug("-==alarm_zone addAlarmInput (NameListLen: %d, GPIOListLen : %d)==-",len(self.zoneInputsGPIOs), len(self.zoneInputsNames))
		return

	def removeAlarmInput(self, AlarmInputGPIO):
		"alarm_zone method used for removing inputs from zone"
		logging.debug("-==alarm_zone removeAlarmInput(GPIO %s)==-", AlarmInputGPIO)
		try:
			idx = self.zoneInputsGPIOs.index(int(AlarmInputGPIO))
		except IndexError:
			logging.error("-==alarm_zone removeAlarmInput(GPIO %s) - element not found! ==-", AlarmInputGPIO)
			return
		self.zoneInputsGPIOs.pop(idx)
		self.zoneInputsNames.pop(idx)
		logging.debug("-==alarm_zone removedAlarmInput (NameListLen: %d, GPIOListLen : %d)==-",len(self.zoneInputsGPIOs), len(self.zoneInputsNames))
		return

def main():
	"main function"
	print "-==alarm_zone: main()==-"
	az = alarm_zone("Zone1")
	az.addAlarmInput("Input1", 1)
	az.addAlarmInput("Input2", 2)
	az.addAlarmInput("Input3", 3)
	az.addAlarmInput("Input5", 5)
	az.addAlarmInput("Input11", 7)
	az.removeAlarmInput(1)
	az.addAlarmInput("Input17", 11)
	az.removeAlarmInput(3)
	az.removeAlarmInput(11)
	#az.removeAlarmInput(17) # test element not in list
	while True:
		time.sleep(1)
	return

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"

