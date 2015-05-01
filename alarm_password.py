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
v 1.5 Fixed the logging initialization; logs are sent to a specific file;
	changed the formatting of log messages

--------------------------------------------------------------------------
"""

import logging						#for logging
import sys						#for logging
from ConfigParser import SafeConfigParser		#for password configuration files
import ConfigParser					#for configuration files
import alarm_keypad					#for alarm_keypad class
import alarm_state					#for alarm_state class

class alarm_password():

	# alarm_password class constants
	alarm_passwords_cfg_file = "alarm_passwords.cfg"
	counter = 0

	def __init__(self):
		# Define alarm_password class variables
		self.num_users = 0
		self.passwd_len = 0
		self.accept_char = ''
		self.clear_char = ''
		self.users_list = []
		self.passwds_list = []
		self.silent_list = []
		self.panic_list = []
		self.attempt = ''

		# Initialize the logging support
		self.initDebugging()

		# Initialize the keypad class
		kp = alarm_keypad.alarm_keypad()

		logging.debug("-==alarm_password: constructor==-")

		# Write the default configuration file to disk
		#self.writePasswordsConfigFile(self.alarm_passwords_cfg_file)

		# Read the class properties from the configuration file
		self.readPasswordsConfigFile(self.alarm_passwords_cfg_file)

		# Chech the class variables values:
		logging.debug("-==alarm_password: number of users: %s==-", self.num_users)
		logging.debug("-==alarm_password: passwords length: %s==-", self.passwd_len)
		logging.debug("-==alarm_password: accept character: %s==-", self.accept_char)
		logging.debug("-==alarm_password: clear character: %s==-", self.clear_char)
		for i in range(0, int(self.num_users)):
			logging.debug("\tUser              %d -> %s", i, self.users_list[i])
			logging.debug("\tArm/Disarm Passwd %d -> %s", i, self.passwds_list[i])
			logging.debug("\tSilent Passwd     %d -> %s", i, self.silent_list[i])
			logging.debug("\tPanic Passwd      %d -> %s\n", i, self.panic_list[i])

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
				cont = 1
				self.counter = 0
				self.attempt = ''
				self.attempt = self.attempt.zfill(int(self.passwd_len))
				logging.debug("CLEAR event: counter: %s, attempt: %s", self.counter, self.attempt)


			# If accept character is pressed the password should be
			# checked in the passwods list
			if digit == self.accept_char:
				cont = 1
				# Check for passcode match
				for i in range (0, int(self.num_users)):
					if (self.attempt == self.passwds_list[i]):
						logging.debug("Correct ARM/DISARM password %s introduced by user %s.", self.attempt, self.users_list[i])
						# Prepairing for the next password, resetting counter and attempt
						self.counter = 0
						self.attempt = ''
						self.attempt = self.attempt.zfill(int(self.passwd_len))
						logging.debug("ACCEPTED ARM/DISARM PASSWORD event: counter: %s, attempt: %s", self.counter, self.attempt)
					if (self.attempt == self.silent_list[i]):
						logging.debug("Correct SILENT password %s introduced by user %s.", self.attempt, self.users_list[i])
						# Prepairing for the next password, resetting counter and attempt
						self.counter = 0
						self.attempt = ''
						self.attempt = self.attempt.zfill(int(self.passwd_len))
						logging.debug("ACCEPTED SILENT PASSWORD event: counter: %s, attempt: %s", self.counter, self.attempt)
					if (self.attempt == self.panic_list[i]):
						logging.debug("Correct PANIC password %s introduced by user %s.", self.attempt, self.users_list[i])
						# Prepairing for the next password, resetting counter and attempt
						self.counter = 0
						self.attempt = ''
						self.attempt = self.attempt.zfill(int(self.passwd_len))
						logging.debug("ACCEPTED PANIC PASSWORD event: counter: %s, attempt: %s", self.counter, self.attempt)
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

			time.sleep(0.2)
		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def writePasswordsConfigFile(self, filename):
		"writing the configuration file for alarm passwords with SafeConfigParser"
		logging.debug("-==alarm_configuration: writePasswordsConfigFile(%s)==-", filename)
		cfgfile = open(filename,'wb')
		try:
			configuration = SafeConfigParser()
			configuration.add_section('GENERAL')
			configuration.set('GENERAL', 'USERS', '3')
			configuration.set('GENERAL', 'LENGTH', '6')
			configuration.set('GENERAL', 'ACCEPT', 'E')
			configuration.set('GENERAL', 'CLEAR', 'C')
			configuration.add_section('PASSWORD_0')
			configuration.set('PASSWORD_0', 'USERNAME', 'User1')
			configuration.set('PASSWORD_0', 'ARM/DISARM PASSWORD', '111111')
			configuration.set('PASSWORD_0', 'SILENT PASSWORD', '999999')
			configuration.set('PASSWORD_0', 'PANIC PASSWORD', '111112')
			configuration.add_section('PASSWORD_1')
			configuration.set('PASSWORD_1', 'USERNAME', 'User2')
			configuration.set('PASSWORD_1', 'ARM/DISARM PASSWORD', '222222')
			configuration.set('PASSWORD_1', 'SILENT PASSWORD', '888888')
			configuration.set('PASSWORD_1', 'PANIC PASSWORD', '222112')
			configuration.add_section('PASSWORD_2')
			configuration.set('PASSWORD_2', 'USERNAME', 'User3')
			configuration.set('PASSWORD_2', 'ARM/DISARM PASSWORD', '987654')
			configuration.set('PASSWORD_2', 'SILENT PASSWORD', '456789')
			configuration.set('PASSWORD_2', 'PANIC PASSWORD', '987112')
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

		self.num_users = configuration.get('GENERAL', 'USERS')
		self.passwd_len = configuration.get('GENERAL', 'LENGTH')
		self.accept_char = configuration.get('GENERAL', 'ACCEPT')
		self.clear_char = configuration.get('GENERAL', 'CLEAR')
		for i in range (0, int(self.num_users)):
			self.users_list.insert(i, configuration.get('PASSWORD_' + str(i), 'USERNAME'))
			self.passwds_list.insert(i, configuration.get('PASSWORD_' + str(i), 'ARM/DISARM PASSWORD'))
			self.silent_list.insert(i, configuration.get('PASSWORD_' + str(i), 'SILENT PASSWORD'))
			self.panic_list.insert(i, configuration.get('PASSWORD_' + str(i), 'PANIC PASSWORD'))

		logging.debug("-==alarm_configuration: readPasswordsConfigFile() exit==-")
		return

def main():
	"main function"
	print "-==alarm_password main()==-"
	# Initialize the passwords class
	passwd = alarm_password()
	return

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
