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

--------------------------------------------------------------------------
"""

from time import sleep
from sys import exit
import alarm_keypad as alarm_kp

class alarm_password():

	# alarm_password class constants
	alarm_passwords_configuration_file = "alarm_password.cfg"
	#attempt = "00000"
	#passcode = "1590E"
	#counter = 0

	def __init__(self):
		# Define alarm_password class variables
		num_users = 0
		passwd_len = 0
		accept_char = ''
		clear_char = ''
		users = []
		passwds = []

		# Initialize the keypad class
		kp = alarm_kp.alarm_keypad()

		# Read the class properties from the configuration file
		self.writePasswordsConfigFile(self.alarm_passwords_configuration_file)
		self.readPasswordsConfigFile(self.alarm_passwords_configuration_file)

		# Chech the class variables values:
		print "number of users: %s"%self.num_users
		print "passwords length: %s"%self.passwd_len
		print "accept character: %s"%self.accept_char
		print "clear character: %s"%self.clear_char
		print users
		print passwds
		attempt = zfill(self.passwd_len + 1)
		print "attempt: %s"%self.attempt

		# Loop while waiting for a keypress
		while True:
			# Loop to get a pressed digit
			digit = None
			while digit == None:
				digit = kp.getKey()
 
			# Print the result
			print "Digit Entered:       %s"%digit
			self.attempt = (self.attempt[1:] + str(digit))
			print "Attempt value:       %s"%self.attempt

			# Check for passcode match
			if (self.attempt == self.passcode):
				print "Your code was correct, goodbye."
				exit()
			else:
				self.counter += 1
				print "Entered digit count: %s"%self.counter
				if (self.counter >= 5):
					print "Incorrect code!"
					sleep(3)
					print "Try Again"
					sleep(1)
					self.counter = 0

			sleep(0.5)

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

			self.num_users = configuration.get('PASSWORDS', 'USERS')
			self.passwd_len = configuration.get('PASSWORDS', 'LENGTH')
			self.accept_char = configuration.get('PASSWORDS', 'ACCEPT')
			self.clear_char = configuration.get('PASSWORDS', 'CLEAR')
			for i in range (0, self.num_users):
				user.insert(i, configuration.get('PASSWORD_' + str(i), 'USERNAME'))
				passwds.insert(i, configuration.get('PASSWORD_' + str(i), 'PASSWORD'))

		except(ConfigObjError, IOError), e:
			logging.error("-==alarm_configuration: readPasswordsConfigFile(): Cannot read %s : %s==-" ,filename, e)
		logging.debug("-==alarm_configuration: readPasswordsConfigFile() exit")
		return

def main():
	"main function"
	print "-==alarm_password main()==-"
	# Initialize the passwords class
	passwd = alarm_password()


if __name__ == '__main__':
	main()
