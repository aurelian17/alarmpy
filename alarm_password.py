#!/usr/bin/env python

"""
alarm_password.py
--------------------------------------------------------------------------

Revision History
v 1.0 First version containing only import of keypad and calls for 
	getting key pressed and validating simple password

--------------------------------------------------------------------------
"""

from time import sleep
from sys import exit
import alarm_keypad as alarm_kp

## Initialize the keypad class.
kp = alarm_kp.keypad()


# Setup variables
attempt = "00000"
passcode = "1590E"
counter = 0

# Loop while waiting for a keypress
while True:
	# Loop to get a pressed digit
	digit = None
	while digit == None:
		digit = kp.getKey()
 
	# Print the result
	print "Digit Entered:       %s"%digit
	attempt = (attempt[1:] + str(digit))  
	print "Attempt value:       %s"%attempt
	
	# Check for passcode match
	if (attempt == passcode):
		print "Your code was correct, goodbye."
		exit()
	else:
		counter += 1
		print "Entered digit count: %s"%counter
		if (counter >= 5):
			print "Incorrect code!"
			sleep(3)
			print "Try Again" 
			sleep(1)
			counter = 0
	
	sleep(0.5)
