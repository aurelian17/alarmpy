#!/usr/bin/env python

"""
alarm_configuration.py
--------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only configuration for alarm inputs

--------------------------------------------------------------------------------
"""

import ConfigParser					#for configuration files
import logging						#for logging
import sys						#for logging


class alarm_configuration():
	# alarm_configuration class constants
	alarm_inputs_filename = "alarm_inputs.cfg"
	alarm_output_filename = "alarm_output.cfg"
	alarm_passwords_filename = "alarm_password.cfg"
	alarm_zones_filename = "alarm_zones.cfg"

	def __init__(self):
		"alarm_configuration class constructor"
		self.initDebugging()
		logging.debug("-==alarm_configuration constructor==-")
		return


	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
		logging.basicConfig(format='%(asctime)s %(message)s')
		logging.basicConfig(datefmt='%m/%d/%Y %I:%M:%S %p')
		return

	def writeInputsConfigFile(self, filename):
		"writing the configuration file for alarm inputs with ConfigParser"
		logging.debug("-==alarm_configuration: writeInputsConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			#configuration.read(filename)
			configuration.add_section('INPUTS')
			configuration.set('INPUTS', 'NUMBER OF INPUTS', '8')
			configuration.set('INPUTS', 'TYPE OF INPUTS', 'PULL_UP')
			configuration.add_section('INPUT_0')
			configuration.set('INPUT_0', 'GPIO_Number', 0)
			configuration.set('INPUT_0', 'GPIO_Timeout', 100)
			configuration.set('INPUT_0', 'GPIO_Edge', 'FALLING')
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_configuration: writeInputsConfigFile(): Cannot read %s:%s==-", filename, err)

		logging.debug("-==alarm_configuration: writeInputsConfigFile() exit==-")
		return

	def readInputsConfigFile(self, filename):
		"reading the configuration file for alarm inputs with ConfigParser"
		logging.debug("-==alarm_configuration: readInputsConfigFile(%s)==-", filename)
		try:
			configuration = ConfigParser.ConfigParser()
			configuration.read(filename)
			print "--------------------------------------------------------------------"
			print configuration
			print "--------------------------------------------------------------------"
			for section in configuration.sections():
				print 'Section: ', section
				print 'Options: ', configuration.options(section)
				for name, value in configuration.items(section):
					print '%s = %s' % (name, value)
				print
		except(ConfigObjError, IOError), e:
			logging.error("-==alarm_configuration: readInputsConfigFile(): Cannot read %s : %s==-" ,filename, e)
		logging.debug("-==alarm_configuration: readInputsConfigFile() exit")
		return

def main():
	"main function"
	ac = alarm_configuration()
	ac.writeInputsConfigFile(ac.alarm_inputs_filename)
	ac.readInputsConfigFile(ac.alarm_inputs_filename)
	return

if __name__ == "__main__":
	main()