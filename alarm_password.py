#!/usr/bin/env python

"""
alarm_password.py
--------------------------------------------------------------------------

Revision History
v 1.0 First version containing only import of keypad and calls for 
	getting key pressed and validating simple password
v 1.1 Added alarm_password class and modified a little the 
	implementation

--------------------------------------------------------------------------
"""

from time import sleep
from sys import exit
import alarm_keypad as alarm_kp

class alarm_password():

	# alarm_password class constants
	attempt = "00000"
	passcode = "1590E"
	counter = 0

	def __init__(self):
		# Initialize the keypad class
		kp = alarm_kp.alarm_keypad()

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

def main():
	"main function"
	print "-==alarm_password main()==-"
	# Initialize the passwords class
	passwd = alarm_password()

if __name__ == '__main__':
	main()
