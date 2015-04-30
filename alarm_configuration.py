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
v 1.5 Added implementation for creating alarm_zone instances based
	on the configuration file
v 1.6 Added initialization of alarm_event class in constructor

--------------------------------------------------------------------------------
"""

import RPi.GPIO as GPIO
import ConfigParser					#for configuration files
from ConfigParser import SafeConfigParser		#for passwords configuration files
import logging						#for logging
import sys						#for logging
import time						#for sleep

import alarm_input
import alarm_zone
import alarm_event

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
	num_zones = 0
	alarm_zones = []

	def __init__(self):
		"alarm_configuration class constructor"
		self.initDebugging()
		logging.debug("-==alarm_configuration constructor==-")
		# initialize the alarm_event class
		alarm_event.alarm_event().getEventInstance()
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
			configuration.add_section('INPUTS')
			configuration.set('INPUTS', 'NUMBER', '3')
			configuration.add_section('INPUT_0')
			configuration.set('INPUT_0', 'GPIO_Number', 1)
			configuration.set('INPUT_0', 'GPIO_Edge', 'FALLING')
			configuration.set('INPUT_0', 'GPIO_Timeout', 100)
			configuration.set('INPUT_0', 'GPIO_Name', 'CONTACT_0')
			configuration.add_section('INPUT_1')
			configuration.set('INPUT_1', 'GPIO_Number', 2)
			configuration.set('INPUT_1', 'GPIO_Edge', 'RISING')
			configuration.set('INPUT_1', 'GPIO_Timeout', 200)
			configuration.set('INPUT_1', 'GPIO_Name', 'CONTACT_1')
			configuration.add_section('INPUT_2')
			configuration.set('INPUT_2', 'GPIO_Number', 3)
			configuration.set('INPUT_2', 'GPIO_Edge', 'BOTH')
			configuration.set('INPUT_2', 'GPIO_Timeout', 300)
			configuration.set('INPUT_2', 'GPIO_Name', 'PIR_0')
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
		logging.debug('-==alarm_configuration: NUMBER INPUTS %s==-', self.num_inputs)
		for i in range (0, int(self.num_inputs)):
			GPIO_Number = configuration.get('INPUT_' + str(i), 'GPIO_Number')
			logging.debug('-==alarm_configuration: ---> INPUT %s: GPIO_Number: %s==-', i, GPIO_Number)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'FALLING':
				GPIO_Edge = GPIO.FALLING
				logging.debug('-==alarm_configuration: ----> GPIO_Edge FALLING: %s==-', GPIO_Edge)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'RISING':
				GPIO_Edge = GPIO.RISING
				logging.debug('-==alarm_configuration: ----> GPIO_Edge RISING: %s==-', GPIO_Edge)
			if configuration.get('INPUT_' + str(i), 'GPIO_Edge') == 'BOTH':
				GPIO_Edge = GPIO.BOTH
				logging.debug('-==alarm_configuration: ----> GPIO_Edge BOTH: %s==-', GPIO_Edge)
			GPIO_Timeout = configuration.get('INPUT_' + str(i), 'GPIO_Timeout')
			logging.debug('-==alarm_configuration: ----->GPIO_Timeout: %s==-', GPIO_Timeout)
			GPIO_Name = configuration.get('INPUT_' + str(i), 'GPIO_Name')
			logging.debug('-==alarm_configuration: ------> GPIO_Name: %s==-', GPIO_Name)
			ai = alarm_input.alarm_input(GPIO_Number, GPIO_Edge, GPIO_Timeout, GPIO_Name)
			self.alarm_inputs.append(ai)
		logging.debug("-==alarm_configuration: alarm_inputs list size %d==-", len(self.alarm_inputs))
		logging.debug("-==alarm_configuration: readInputsConfigFile() exit==-")
		return


	def writeZonesConfigFile(self, filename):
		"writing the configuration file for alarm zones with ConfigParser"
		logging.debug("-==alarm_configuration: writeZonesConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			configuration.add_section('ZONES')
			configuration.set('ZONES', 'NUMBER', '2')
			configuration.add_section('ZONE_0')
			configuration.set('ZONE_0', 'Name', 'Zone0')
			configuration.set('ZONE_0', 'Inputs', 1)
			configuration.set('ZONE_0', 'Input_0', 'PIR_0')
			configuration.add_section('ZONE_1')
			configuration.set('ZONE_1', 'Name', 'Zone1')
			configuration.set('ZONE_1', 'Inputs', 2)
			configuration.set('ZONE_1', 'Input_0', 'CONTACT_0')
			configuration.set('ZONE_1', 'Input_1', 'CONTACT_1')
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_configuration: writeInputsConfigFile(): Cannot read %s:%s==-", filename, err)

		logging.debug("-==alarm_configuration: writeInputsConfigFile() exit==-")
		return


	def readZonesConfigFile(self, filename):
		"reading the configuration file for alarm zones with ConfigParser"
		logging.debug("-==alarm_configuration: readZonesConfigFile(%s)==-", filename)
		configuration = ConfigParser.ConfigParser()
		configuration.read(filename)
		self.num_zones = configuration.get('ZONES', 'NUMBER')
		logging.debug('-==alarm_configuration: NUMBER ZONES %s==-', self.num_zones)
		for i in range (0, int(self.num_zones)):
			zoneName = configuration.get('ZONE_' + str(i), 'Name')
			zoneInputs = configuration.get('ZONE_' + str(i), 'Inputs')
			logging.debug('-==alarm_configuration: --->Zone %d : %s %s input(s)==-', i, zoneName, zoneInputs)
			az = alarm_zone.alarm_zone(zoneName, zoneInputs)
			for j in range (0, int(zoneInputs)):
				inputName = configuration.get('ZONE_' + str(i), 'Input_' + str(j))
				logging.debug("-==alarm_configuration: ----> Zone_%d: Input_%d - %s==-", i, j, zoneName)
				lst = filter(lambda x: x.GPIO_Name == inputName, self.alarm_inputs)
				if len(lst) == 1:
					ai = lst.pop()
				else:
					logging.error("-==alarm_configuration more than one input with name %s entered!==-", inputName)
					break
				ai.setZone(zoneName)
				az.addAlarmInput(ai.GPIO_Name, ai.GPIO_Number)
			self.alarm_zones.append(az)
		logging.debug("-==alarm_configuration: alarm_zones list size %d==-", len(self.alarm_zones))
		logging.debug("-==alarm_configuration: readZonesConfigFile() exit==-")
		return

def main():
	"main function"
	print "-==alarm_configuration: main()==-"
	ac = alarm_configuration()
	#ac.writeInputsConfigFile(ac.alarm_inputs_filename)
	ac.readInputsConfigFile(ac.alarm_inputs_filename)
	#ac.writeZonesConfigFile(ac.alarm_zones_filename)
	ac.readZonesConfigFile(ac.alarm_zones_filename)
	while True:
		time.sleep(1)
	return

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"

