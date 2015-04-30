#!/usr/bin/env python

"""
alarm_event.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation for singleton pattern
v 1.1 Added support for configuration file
v 1.2 Added support for sending e-mail in case of alarm events

----------------------------------------------------------------------------------------
"""


import time						#for sleep
import logging						#for logging
import sys						#for logging
import ConfigParser					#for configuration files
import thread						#for multithreading support
import smtplib						#for sending e-mail support
from email.mime.text import MIMEText			#for sending e-mail support
from email.mime.multipart import MIMEMultipart		#for sending e-mail support


"""
  http://www.mindviewinc.com/Books/Python3Patterns/Index.php
"""
class Singleton:
	def __init__(self, klass):
		self.klass = klass
		self.instance = None
		return;

	def __call__(self, *args, **kwds):
		if self.instance == None:
			self.instance = self.klass(*args, **kwds)
		return self.instance

@Singleton
class alarm_event(object):
	# alarm_event class constants
	INSTANCE = None

	alarm_events_filename = "alarm_events.cfg"

	# database related constants
	enableDatabase = False
	databasePath = ''
	databaseFilename = ''

	# SMTP notification related constants
	enableSMTP = False
	serverSMTP = ''
	userSMTP = ''
	passwordSMTP = ''
	typeSMTP = ''
	portSMTP = 0

	# notification recipients related constants
	recipientsNumber = 0
	recipients = []

	def __init__(self):
		"alarm_event class constructor"

		#initialize the debugging system
		self.initDebugging()
		logging.debug("-==alarm_event constructor %s==-", self)

		if self.INSTANCE is not None:
			raise ValueError("An alarm_event instantiation already exists!")

		#self.writeEventsConfigFile(self.alarm_events_filename)
		self.readEventsConfigFile(self.alarm_events_filename)

		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def writeEventsConfigFile(self, filename):
		"writing the configuration file for alarm_events with ConfigParser"
		logging.debug("-==alarm_event: writeEentsConfigFile(%s) ==-", filename)
		cfgfile = open(filename, 'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			configuration.add_section('GENERAL')
			configuration.set('GENERAL', 'USE DATABASE', False)
			configuration.set('GENERAL', 'USE MAIL NOTIFICATION', True)
			configuration.add_section('DATABASE')
			configuration.set('DATABASE', 'PATH', '/home/pi/alarmpy/')
			configuration.set('DATABASE', 'FILENAME', 'events.db')
			configuration.add_section('E-MAIL')
			configuration.set('E-MAIL', 'SMTP SERVER', 'smtp.gmail.com')
			configuration.set('E-MAIL', 'SMTP USER', 'user@gmail.com')
			configuration.set('E-MAIL', 'SMTP PASSWORD', 'password')
			# SMTP Type can be NONE/SSL/TLS
			configuration.set('E-MAIL', '## = SMTP TYPE can be NONE/SSL/TLS', '##')
			configuration.set('E-MAIL', 'SMTP TYPE', 'SSL')
			# SMTP Port can be NONE/465/587
			configuration.set('E-MAIL', '## = SMTP PORT can be NONE/465/587', '##')
			configuration.set('E-MAIL', 'SMTP PORT', 465)
			configuration.add_section('NOTIFICATION RECIPIENTS')
			configuration.set('NOTIFICATION RECIPIENTS', 'NUMBER', 2)
			configuration.set('NOTIFICATION RECIPIENTS', 'RECIPIENT_0', 'recipient@gmail.com')
			configuration.set('NOTIFICATION RECIPIENTS', 'RECIPIENT_1', 'recipient@yahoo.com')
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_event: writeEventsConfigFile(): Cannot read %s:%s ==-", filename, error)

		logging.debug("-==alarm_event: writeEventsConfigFile() exit ==-")

	def readEventsConfigFile(self, filename):
		"reading the configuration file for alarm events with ConfigParser"
		logging.debug("-==alarm_event: readEventsConfigFile(%s)==-", filename)
		configuration = ConfigParser.ConfigParser()
		configuration.read(filename)

		self.enableDatabase = configuration.get('GENERAL', 'USE DATABASE')
		self.enableSMTP = configuration.get('GENERAL', 'USE MAIL NOTIFICATION')
		logging.debug('-==alarm_event: readEventsConfigFile(): USE DATABASE %s - USE MAIL NOTIFICATION %s==-', self.enableDatabase, self.enableSMTP)

		self.databasePath = configuration.get('DATABASE', 'PATH')
		self.databaseFilename = configuration.get('DATABASE', 'FILENAME')
		logging.debug('-==alarm_event: readEventsConfigFile(): DATABASE: Path %s - Filename %s==-', self.databasePath, self.databaseFilename)

		self.serverSMTP = configuration.get('E-MAIL', 'SMTP SERVER')
		self.userSMTP = configuration.get('E-MAIL', 'SMTP USER')
		self.passwordSMTP = configuration.get('E-MAIL','SMTP PASSWORD')
		self.typeSMTP = configuration.get('E-MAIL', 'SMTP TYPE')
		self.portSMTP = configuration.get('E-MAIL','SMTP PORT')
		logging.debug('-==alarm_event: readEventsConfigFile(): SMTP: Server %s - User %s - Password %s - Type %s - Port %s==-', self.serverSMTP, self.userSMTP, self.passwordSMTP, self.typeSMTP, self.portSMTP)

		self.recipientsNumber = configuration.get('NOTIFICATION RECIPIENTS', 'NUMBER')
		logging.debug('-==alarm_event: readEventsConfigFile(): NOTIFICATION RECIPIENTS NUMBER %s==-', self.recipientsNumber)

		for i in range (0, int(self.recipientsNumber)):
			recipient = configuration.get('NOTIFICATION RECIPIENTS', 'RECIPIENT_' + str(i))
			logging.debug('-==alarm_event: readEventsConfigFile(): NOTIFICATION RECIPIENT %d: %s==-', i, recipient)
			self.recipients.append(recipient)

		logging.debug("-==alarm_event: readEventConfigFile() exit==-")
		return

	def getEventInstance(cls):
		"Return the alarm_event single class instance"
		if cls.INSTANCE is None:
			cls.INSTANCE = alarm_event()
		return cls.INSTANCE

	def insertEvent(self, inputName, inputZone, inputGPIO):
		"Add a new alarm_event"
		logging.debug("-==alarm_event insertEvent: inputName: %s, inputZone: %s, inputGPIO: %s ==-", inputName, inputZone, inputGPIO)
		if self.enableSMTP == 'True':
			self.sendEventNotificationEmail(inputName, inputZone, inputGPIO)
		return

	def sendEventNotificationEmailThread(self, inputName, inputZone, inputGPIO):
		"Send event notification e-mail to all recipients list from a separate thread"
		logging.debug("-==alarm_event sendEventNotificationEmailThread: inputName: %s, inputZone: %s, inputGPIO: %s ==-", inputName, inputZone, inputGPIO)
		try:
			thread.start_new_thread(sendEventNotificationEmail, (inputName, inputZone, inputGPIO))
		except:
			logging.error("-==alarm_event sendEventNotificationEmailThread: Unable to start thread!!!==-")
		return

	def sendEventNotificationEmail(self, inputName, inputZone, inputGPIO):
		"Send event notification e-mail to all recipients list"
		logging.debug("-==alarm_event sendEventNotificationEmail: inputName: %s, inputZone: %s, inputGPIO: %s ==-", inputName, inputZone, inputGPIO)

		for i in range (0, int(self.recipientsNumber)):
			messageText = "This is an automated alarm notification e-mail from AlarmPi System for:\nHome Alarm System triggered in:\n\tZone: " + inputZone + "\n\tSensor: " + inputName + "\n\tGPIO: " + str(inputGPIO)

			message = MIMEText(messageText)

			message['To'] = self.recipients[i]
			message['From'] = self.userSMTP
			message['Subject'] = "AlarmPI Notification"

			# No Encryption
			if str(self.typeSMTP).lower() == str('NONE').lower():
				session = smtplib.SMTP(self.serverSMTP)

			# SSL Encryption
			elif str(self.typeSMTP).lower() == str('SSL').lower():
				session = smtplib.SMTP_SSL(self.serverSMTP, 465)

			# TLS Encryption
			elif str(self.typeSMTP).lower() == str('TLS').lower():
				session = smtlib.SMTP(self.serverSMTP, 587)
				session.ehlo()
				session.starttls()
				session.ehlo
			else:
				session = smtplib.SMTP(self.serverSMTP)

			#session.set_debuglevel(True)
			#session.verify(self.recipients[i])
			session.login(self.userSMTP, self.passwordSMTP)
			try:
				session.sendmail(self.userSMTP, self.recipients[i], message.as_string())
			except:
				logging.error("-==alarm_event sendEentNotificationEmail(): Failed to send the mail to %s==-", self.recipients[i])

			session.quit()
			session.close()

		logging.debug("-==alarm_event sendEventNotificationEmail() exit==-")
		return

	def __del__(self):
		"clean up the alarm_event on normal exit"
		logging.debug("-==alarm_event destructor()==-")
		return

def main():
	"main function"
	print "-==alarm_event main()==-"
	# Initialize the alarm_input class
	ae1 = alarm_event().getEventInstance()
	ae2 = alarm_event().getEventInstance()
	ae3 = alarm_event().getEventInstance()

	ae1.insertEvent("GPIO_1", "Zone0", 17)
	ae3.insertEvent("GPIO_3", "Zone0", 22)
	ae2.insertEvent("GPIO_2", "Zone1", 21)

	ae1.insertEvent("GPIO_1", "Zone0", 17)
	ae2.insertEvent("GPIO_2", "Zone1", 21)
	ae3.insertEvent("GPIO_3", "Zone0", 22)

	ae2.insertEvent("GPIO_2", "Zone1", 21)
	ae3.insertEvent("GPIO_3", "Zone0", 22)
	ae1.insertEvent("GPIO_1", "Zone0", 17)

	while True:
		time.sleep(1)
	return


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
