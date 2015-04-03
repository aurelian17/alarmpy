#!/usr/bin/env python

"""
alarm_configuration.py
--------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only configuration for alarm inputs
v 1.1 Added configuration for alarm passwords

--------------------------------------------------------------------------------
"""
import RPi.GPIO as GPIO
import ConfigParser					#for configuration files
from ConfigParser import SafeConfigParser		#for passwords configuration files
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
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		return

	def writeInputsConfigFile(self, filename):
		"writing the configuration file for alarm inputs with ConfigParser"
		logging.debug("-==alarm_configuration: writeInputsConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			#configuration.read(filename)
			configuration.add_section('INPUTS')
			configuration.set('INPUTS', 'NUMBER', '8')
			configuration.add_section('INPUT_0')
			configuration.set('INPUT_0', 'GPIO_Number', 0)
			configuration.set('INPUT_0', 'GPIO_Pull', GPIO.PUD_UP)
			configuration.set('INPUT_0', 'GPIO_Edge', GPIO.FALLING)
			configuration.set('INPUT_0', 'GPIO_Timeout', 100)
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


	def writePasswordsConfigFile(self, filename):
		"writing the configuration file for alarm passwords with ConfigParser"
		logging.debug("-==alarm_configuration: writePasswordsConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = SafeConfigParser()
			configuration.add_section('PASSWORDS')
			configuration.set('PASSWORDS', 'USERS', '3')
			configuration.set('PASSWORDS', 'LENGTH', '4')
			configuration.set('PASSWORDS', 'ACCEPT', 'E')
			configuration.set('PASSWORDS', 'CLEAR', 'C')
			configuration.add_section('PASSWORD_0')
			configuration.set('PASSWORD_0', 'USERNAME', 'User0')
			configuration.set('PASSWORD_0', 'PASSWORD', '0000')
			configuration.add_section('PASSWORD_1')
			configuration.set('PASSWORD_1', 'USERNAME', 'User1')
			configuration.set('PASSWORD_1', 'PASSWORD', '1111')
			configuration.add_section('PASSWORD_2')
			configuration.set('PASSWORD_2', 'USERNAME', 'User2')
			configuration.set('PASSWORD_2', 'PASSWORD', '2222')
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_configuration: writePasswordsConfigFile(): Cannot read %s:%s==-", filename, err)

		logging.debug("-==alarm_configuration: writePasswordsConfigFile() exit==-")
		return

	def readPasswordsConfigFile(self, filename):
		"reading the configuration file for alarm passwords with ConfigParser"
		logging.debug("-==alarm_configuration: readPasswordsConfigFile(%s)==-", filename)
		try:
			configuration = SafeConfigParser()
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
			logging.error("-==alarm_configuration: readPasswordsConfigFile(): Cannot read %s : %s==-" ,filename, e)
		logging.debug("-==alarm_configuration: readPasswordsConfigFile() exit")
		return

def main():
	"main function"
	logging.debug("-==alarm_configuration: main()==-"
	ac = alarm_configuration()
	ac.writeInputsConfigFile(ac.alarm_inputs_filename)
	ac.readInputsConfigFile(ac.alarm_inputs_filename)
	ac.writePasswordsConfigFile(ac.alarm_passwords_filename)
	ac.readPasswordsConfigFile(ac.alarm_passwords_filename)
	return

if __name__ == "__main__":
	main()
