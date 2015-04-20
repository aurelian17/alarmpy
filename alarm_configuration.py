#!/usr/bin/env python

"""
alarm_configuration.py
--------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only configuration for alarm inputs
v 1.1 Added configuration for alarm passwords
v 1.2 Moved the password configuration in the alarm_password class
v 1.4 Added implementation for creating alarm_input instances based
	on the configuration file

--------------------------------------------------------------------------------
"""

import RPi.GPIO as GPIO
import ConfigParser					#for configuration files
from ConfigParser import SafeConfigParser		#for passwords configuration files
import logging						#for logging
import sys						#for logging
import time						#for sleep

import alarm_input

class alarm_configuration():
	# alarm_configuration class constants

	# alarm_inputs specific constants
	alarm_inputs_filename = "alarm_inputs.cfg"
	num_inputs = 0
	alarm_inputs = []

	# alarm_outputs specific constants
	alarm_output_filename = "alarm_output.cfg"

	#alarm_zones specific constants
	alarm_zones_filename = "alarm_zones.cfg"

	def __init__(self):
		"alarm_configuration class constructor"
		self.initDebugging()
		logging.debug("-==alarm_configuration constructor==-")
		return


	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def writeInputsConfigFile(self, filename):
		"writing the configuration file for alarm inputs with ConfigParser"
		logging.debug("-==alarm_configuration: writeInputsConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			#configuration.read(filename)
			configuration.add_section('INPUTS')
			configuration.set('INPUTS', 'NUMBER', '3')
			configuration.add_section('INPUT_0')
			configuration.set('INPUT_0', 'GPIO_Number', 0)
			configuration.set('INPUT_0', 'GPIO_Edge', 'FALLING')
			configuration.set('INPUT_0', 'GPIO_Timeout', 100)
			configuration.add_section('INPUT_1')
			configuration.set('INPUT_1', 'GPIO_Number', 1)
			configuration.set('INPUT_1', 'GPIO_Edge', 'RISING')
			configuration.set('INPUT_1', 'GPIO_Timeout', 200)
			configuration.add_section('INPUT_2')
			configuration.set('INPUT_2', 'GPIO_Number', 2)
			configuration.set('INPUT_2', 'GPIO_Edge', 'BOTH')
			configuration.set('INPUT_2', 'GPIO_Timeout', 300)
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_configuration: writeInputsConfigFile(): Cannot read %s:%s==-", filename, err)

		logging.debug("-==alarm_configuration: writeInputsConfigFile() exit==-")
		return

	def readInputsConfigFile(self, filename):
		"reading the configuration file for alarm inputs with ConfigParser"
		logging.debug("-==alarm_configuration: readInputsConfigFile(%s)==-", filename)
		configuration = ConfigParser.ConfigParser()
		configuration.read(filename)
		self.num_inputs = configuration.get('INPUTS', 'NUMBER')
		logging.debug('-==alarm_configuration: NUMBER INPUTS %s', self.num_inputs)
		for i in range (0, int(self.num_inputs)):
			GPIO_Number = configuration.get('INPUT_' + str(i), 'GPIO_Number')
			logging.debug('-==alarm_configuration: --->INPUT %s GPIO_Number: %s', i, GPIO_Number)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'FALLING':
				GPIO_Edge = GPIO.FALLING
				logging.debug('-==alarm_configuration: ---->GPIO_Edge FALLING: %s', GPIO_Edge)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'RISING':
				GPIO_Edge = GPIO.RISING
				logging.debug('-==alarm_configuration: ---->GPIO_Edge RISING: %s', GPIO_Edge)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'BOTH':
				GPIO_Edge = GPIO.BOTH
				logging.debug('-==alarm_configuration: ---->GPIO_Edge BOTH: %s', GPIO_Edge)
			GPIO_Timeout = configuration.get('INPUT_' + str(i), 'GPIO_Timeout')
			logging.debug('-==alarm_configuration: ----->GPIO_Timeout: %s', GPIO_Timeout)
			ai = alarm_input.alarm_input(GPIO_Number, GPIO_Edge, GPIO_Timeout)
			self.alarm_inputs.append(ai)
		logging.debug("-==alarm_configuration: alarm_inputs list size %d", len(self.alarm_inputs))
		logging.debug("-==alarm_configuration: readInputsConfigFile() exit")
		return

def main():
	"main function"
	print "-==alarm_configuration: main()==-"
	ac = alarm_configuration()
	#ac.writeInputsConfigFile(ac.alarm_inputs_filename)
	ac.readInputsConfigFile(ac.alarm_inputs_filename)
	while True:
		time.sleep(1)
	return

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"

