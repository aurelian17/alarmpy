#!/usr/bin/env python

"""
alarm_state.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation for singleton pattern

----------------------------------------------------------------------------------------
"""


import time						#for sleep
import logging						#for logging
import sys						#for logging
import ConfigParser					#for configuration files
from multiprocessing import Process, Lock, Value	#for multiprocessing

"""
  http://www.mindviewinc.com/Books/Python3Patterns/Index.php
"""
class StateSingleton:
	# define the states of the alarm system

	# DISARMED - the system is disarmed, the sensors will not be read
	# ARMED - the system is armed, when intrusion event detected siren will ring
	# SILENT - the system is armed, when intrusion event detected only notification will be sent,
	#          the siren will not ring
	# PANIC - the system is in any state, panic event occurs, after a timeout,
	#         the siren will ring and notifications will be sent
	DISARMED, ARMED, SILENT, PANIC = range(0, 4)

	def __init__(self, klass):
		self.klass = klass
		self.instance = None
		self.lock = Lock()
		return

	def __call__(self, *args, **kwds):
		if self.instance == None:
			with self.lock:
				if self.instance == None:
					self.instance = self.klass(*args, **kwds)
		return self.instance


@StateSingleton
class alarm_state(object):
	# alarm_state class constants
	INSTANCE = None
	mutex = Lock()

	# database related constants
	databaseEnabled = False
	databasePath = ''
	databaseFilename = ''
	databaseTable = ''

	alarm_states_filename = "alarm_states.cfg"

	def __init__(self):
		"alarm_state class constructor"

		#initialize the debugging system
		self.initDebugging()
		logging.debug("-==alarm_state constructor %s==-", self)

		if self.INSTANCE is not None:
			raise ValueError("An alarm_state instantiation already exists!")

		self.state = Value('i', 0) # system is initialized in state DISARMED

		#self.writeStatesConfigFile(self.alarm_states_filename)
		self.readStatesConfigFile(self.alarm_states_filename)
		return

	def initDebugging(self):
		"initialization of the debugging system"
		logging.basicConfig(level=logging.DEBUG,
				    format='%(asctime)s.%(msecs).03d - %(levelname)s : %(message)s',
				    datefmt='%d/%m/%Y %H:%M:%S',
				    filename='alarm_log.log',
				    filemode='w')
		return

	def writeStatesConfigFile(self, filename):
		"writing the configuration file for alarm_states with ConfigParser"
		logging.debug("-==alarm_state: writeStatesConfigFile(%s) ==-", filename)
		cfgfile = open(filename, 'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			configuration.add_section('GENERAL')
			configuration.set('GENERAL', 'USE DATABASE', False)
			configuration.add_section('DATABASE')
			configuration.set('DATABASE','PATH','/home/pi/alarmpy/')
			configuration.set('DATABASE','FILENAME','alarmSystem.db')
			configuration.set('DATABASE','TABLE','States')
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_state: writeStatesConfigFile(): Cannot read %s:%s ==-", filename, error)

		logging.debug("-==alarm_state: writeStatesConfigFile() exit ==-")
		return

	def readStatesConfigFile(self, filename):
		"reading the configuration file for alarm_states with ConfigParser"
		logging.debug("-==alarm_state: readStatesConfigFile(%s)==-", filename)
		configuration = ConfigParser.ConfigParser()
		configuration.read(filename)

		self.databaseEnabled = configuration.get('GENERAL', 'USE DATABASE')
		logging.debug('-==alarm_state: readStatesConfigFile(): USE DATABASE %s==-', self.databaseEnabled)

		self.databasePath = configuration.get('DATABASE', 'PATH')
		self.databaseFilename = configuration.get('DATABASE', 'FILENAME')
		self.databaseTable = configuration.get('DATABASE', 'TABLE')
		logging.debug('-==alarm_state: readStatesConfigFile(): DATABASE: Path %s - Filename %s - Table %s==-', self.databasePath, self.databaseFilename, self.databaseTable)

		logging.debug("-==alarm_event: readStatesConfigFile() exit==-")
		return

	def getStateInstance(cls):
		"Return the alarm_state single class instance"
		if cls.INSTANCE is None:
			cls.INSTANCE = alarm_state()
		return cls.INSTANCE

	def setState(self, newState):
		"Change the state field from alarm_state class protected with mutex"
		with self.mutex:
			self.state.value = newState
		return

	def getState(self):
		"Get the state field from alarm_state class protected with mutex"
		with self.mutex:
			return self.state.value

	def stateToString(self, newState):
		"Returning the string of the newState received as parameter"
		strState = ''
		if alarm_state.ARMED == newState:
			strState = "ARMED"
		if alarm_state.DISARMED == newState:
			strState = "DISARMED"
		if alarm_state.SILENT == newState:
			strState = "SILENT"
		if alarm_state.PANIC == newState:
			strState = "PANIC"
		return strState

	def changeState(self, newState, fromUser):
		"Change the alarm system state and save the event to database from a separate process"
		logging.debug("-==alarm_state changeState: from %s to %s - from user %s==-", self.stateToString(self.getState()), self.stateToString(newState), fromUser)
		if alarm_state.ARMED == newState:
			if self.getState() != alarm_state.ARMED:
				self.setState(newState)

		if alarm_state.DISARMED == newState:
			if self.getState() == alarm_state.ARMED or self.getState() == alarm_state.SILENT:
				self.setState(newState)

		if alarm_state.SILENT == newState:
			if self.getState() == alarm_state.DISARMED or self.getState() == alarm_state.ARMED:
				self.setState(newState)

		#if alarm_state.PANIC == newState:
		# doing nothing at this moment in case of PANIC, will be updated in the future

		logging.debug("-==alarm_state changeState: newState %s by %s==-", self.stateToString(self.getState()), fromUser)

		if self.databaseEnabled == 'True':
			try:
				process = Process(target = self.changeStateOperation, args = (newState, fromUser))
				process.start()
			except:
				logging.error("-==alarm_state startChangeStateThread: Unable to start change state thread!!!==-")

		return

	def changeStateOperation(self, newState, fromUser):
		"Save the alarm change state event to database"
		logging.debug("-==alarm_state changeStateOperation: state: %s - from user %s==-", newState, fromUser)
		logging.debug("-==alarm_state changeStateOperation() exit==-")
		return

	def __del__(self):
		"clean up the alarm_state on normal exit"
		logging.debug("-==alarm_state destructor()==-")
		return

def main():
	"main function"
	print "-==alarm_state main()==-"
	# Initialize the alarm_state class
	almst = alarm_state().getStateInstance()

	# Start 3 different processes in order to make change state operations in the same time
	prcs1 = Process(target = process1, args = ('prc1', 'user1'))
	prcs2 = Process(target = process2, args = ('prc2', 'user2'))
	prcs3 = Process(target = process3, args = ('prc3', 'user3'))
	prcs1.start()
	prcs2.start()
	prcs3.start()

	while True:
		time.sleep(1)
	return

def process1(processName, userName):
	print ("Process: %s started for: %s"% (processName, userName))
	as1 = alarm_state().getStateInstance()
	time.sleep(0.8)
	as1.changeState(alarm_state.ARMED, userName)
	time.sleep(0.1)
	as1.changeState(alarm_state.DISARMED, userName)
	time.sleep(0.1)
	as1.changeState(alarm_state.DISARMED, userName)
	time.sleep(1)
	print ("Process: %s at the END: %s from user: %s"% (processName, as1.stateToString(as1.getState()), userName))
	return

def process2(processName, userName):
	print ("Process: %s started for: %s"% (processName, userName))
	as2 = alarm_state().getStateInstance()
	time.sleep(0.85)
	as2.changeState(alarm_state.SILENT, userName)
	time.sleep(0.05)
	as2.changeState(alarm_state.SILENT, userName)
	time.sleep(0.1)
	as2.changeState(alarm_state.ARMED, userName)
	time.sleep(1)
	print ("Process: %s at the END: %s from user: %s"% (processName, as2.stateToString(as2.getState()), userName))
	return

def process3(processName, userName):
	print ("Process: %s started for: %s"% (processName, userName))
	as3 = alarm_state().getStateInstance()
	time.sleep(0.88)
	as3.changeState(alarm_state.ARMED, userName)
	time.sleep(0.02)
	as3.changeState(alarm_state.PANIC, userName)
	time.sleep(0.1)
	as3.changeState(alarm_state.SILENT, userName)
	time.sleep(1)
	print ("Process: %s at the END: %s from user: %s"% (processName, as3.stateToString(as3.getState()), userName))
	return

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
