#!/usr/bin/env python

"""
alarm_password.py
--------------------------------------------------------------------------

Revision History
v 1.0 First version containing only import of keypad and calls for 
	getting key pressed and validating simple password
v 1.1 Added alarm_password class and modified a little the 
	implementation
v 1.2 Added implementation for reading class constants from configuration
	file
v 1.3 Added implementation for comparing with all passwords stored in the
	configuration file
v 1.4 Added logging support for alarm_password class

--------------------------------------------------------------------------
"""

from time import sleep
from sys import exit
import logging						#for logging
import sys						#for logging
from ConfigParser import SafeConfigParser		#for password configuration files
import ConfigParser					#for configuration files
import alarm_keypad as alarm_kp

class alarm_password():

	# alarm_password class constants
	alarm_passwords_cfg_file = "alarm_password.cfg"
	counter = 0

	def __init__(self):
		# Define alarm_password class variables
		self.num_users = 0
		self.passwd_len = 0
		self.accept_char = ''
		self.clear_char = ''
		self.users_list = []
		self.passwds_list = []
		self.attempt = ''

		# Initialize the logging support
		self.initDebugging()

		# Initialize the keypad class
		kp = alarm_kp.alarm_keypad()

		logging.debug("-==alarm_password constructor==-")

		# Read the class properties from the configuration file
		self.readPasswordsConfigFile(self.alarm_passwords_cfg_file)

		# Chech the class variables values:
		logging.debug("number of users: %s", self.num_users)
		logging.debug("passwords length: %s", self.passwd_len)
		logging.debug("accept character: %s", self.accept_char)
		logging.debug("clear character: %s", self.clear_char)
		for i in range(0, int(self.num_users)):
			logging.debug("User %d -> %s", i, self.users_list[i])
			logging.debug("Pass %d -> %s", i, self.passwds_list[i])

		self.attempt = self.attempt.zfill(int(self.passwd_len))
		logging.debug("attempt: %s", self.attempt)

		# Loop while waiting for a keypress
		while True:
			cont = 0
			# Loop to get a pressed digit
			digit = None
			while digit == None:
				digit = kp.getKey()

			logging.debug("Digit Entered: %s", digit)
			logging.debug("Entered digit count: %s", self.counter)
			logging.debug("Attempt value: %s", self.attempt)

			# If clear character is pressed all the history until this
			# point should be cleared
			if digit == self.clear_char:
				logging.debug("Clear keypad pressed")
				cont = 1
				self.counter = 0
				self.attempt = ''
				self.attempt = self.attempt.zfill(int(self.passwd_len))
				logging.debug("CLEAR event: counter: %s, attempt: %s", self.counter, self.attempt)


			# If accept character is pressed the password should be
			# checked in the passwods list
			if digit == self.accept_char:
				logging.debug("Enter keypad pressed")
				cont = 1
				# Check for passcode match
				for i in range (0, int(self.num_users)):
					if (self.attempt == self.passwds_list[i]):
						logging.debug("Correct passwod %s introduced by user %s.", self.attempt, self.users_list[i])
						# Prepairing for the next password, resetting counter and attempt
						self.counter = 0
						self.attempt = ''
						self.attempt = self.attempt.zfill(int(self.passwd_len))
						logging.debug("ACCEPTED PASSWORD event: counter: %s, attempt: %s", self.counter, self.attempt)
				self.counter = 0
				self.attempt = ''
				self.attempt = self.attempt.zfill(int(self.passwd_len))
				logging.debug("ACCEPT event: counter: %s, attempt: %s", self.counter, self.attempt)


			if cont != 1:
				# Concatenate the last valid character to attempt and increment counter
				self.attempt = (self.attempt[1:] + str(digit))
				self.counter += 1

			# More than password length + 1 ending characters entered
			if int(self.counter) > int(self.passwd_len) + 1:
				# No correct password entered and the number of characters entered exeeded the
				# password length
				self.counter = 0
				self.attempt = ''
				self.attempt = self.attempt.zfill(int(self.passwd_len))
				logging.debug("EXCEED event: counter: %s, attempt: %s", self.counter, self.attempt)

			sleep(0.2)
		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(sstram=sys.stderr, level=logging.DEBUG)
		logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		return

	def writePasswordsConfigFile(self, filename):
		"writing the configuration file for alarm passwords with SafeConfigParser"
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
		"reading the configuration file for alarm passwords with SafeConfigParser"
		logging.debug("-==alarm_configuration: readPasswordsConfigFile(%s)==-", filename)
		configuration = SafeConfigParser()
		configuration.read(filename)

		self.num_users = configuration.get('PASSWORDS', 'USERS')
		self.passwd_len = configuration.get('PASSWORDS', 'LENGTH')
		self.accept_char = configuration.get('PASSWORDS', 'ACCEPT')
		self.clear_char = configuration.get('PASSWORDS', 'CLEAR')
		for i in range (0, int(self.num_users)):
			self.users_list.insert(i, configuration.get('PASSWORD_' + str(i), 'USERNAME'))
			self.passwds_list.insert(i, configuration.get('PASSWORD_' + str(i), 'PASSWORD'))

		logging.debug("-==alarm_configuration: readPasswordsConfigFile() exit")
		return

def main():
	"main function"
	print "-==alarm_password main()==-"
	# Initialize the passwords class
	passwd = alarm_password()


if __name__ == '__main__':
	main()
