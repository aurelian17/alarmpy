#!/usr/bin/env python

"""
alarm_DVR.py
----------------------------------------------------------------------------------------

Revision History
v 1.0 First version containing only implementation

----------------------------------------------------------------------------------------
"""


import time						#for sleep
import logging						#for logging
import sys						#for logging
import ConfigParser					#for configuration files
import socket						#for socket listening
import threading					#for multithreading

from multiprocessing import Process, Lock, Value	#for multiprocessing

host = '127.0.0.1'
port = 50000

"""
  http://www.mindviewinc.com/Books/Python3Patterns/Index.php
"""
class StateSingleton:
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
class alarm_DVR(threading.Thread):
	# alarm_DVR class constants

	INSTANCE = None
	mutex = Lock()

	# DVR related constants
	hostDVR = '127.0.0.1'
	portDVR = 50000

	alarm_states_filename = "alarm_DVR.cfg"

	def __init__(self, conn):
		"alarm_DVR class constructor"
		super(client, self).__init__()
		self.conn = conn
		self.data = ""

		#initialize the debugging system
		self.initDebugging()
		logging.debug("-==alarm_DVR constructor %s==-", self)

		if self.INSTANCE is not None:
			raise ValueError("An alarm_DVR instantiation already exists!")

		#self.writeStatesConfigFile(self.alarm_states_filename)
		self.readStatesConfigFile(self.alarm_states_filename)
		return

	def run(self):
		while True:
			self.data = self.data + self.conn.recv(1024)
			if self.data.endswith(u"\r\n"):
				print self.data
				self.data = ""
		return

	def sendMessage(self, msg):
		self.conn.send(msg)
		return

	def close(self):
		self.conn.close()
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
		"writing the configuration file for alarm_DVR with ConfigParser"
		logging.debug("-==alarm_DVR: writeStatesConfigFile(%s) ==-", filename)
		cfgfile = open(filename, 'wb')
		try:
			configuration = ConfigParser.ConfigParser()
			configuration.add_section('GENERAL')
			configuration.set('GENERAL', 'HOST', '127.0.0.1')
			configuration.set('GENERAL', 'PORT', 50000)
			configuration.write(cfgfile)
			cfgfile.close()

		except ConfigParser.ParsingError, err:
			logging.error("-==alarm_DVR: writeStatesConfigFile(): Cannot read %s:%s ==-", filename, error)

		logging.debug("-==alarm_DVR: writeStatesConfigFile() exit ==-")
		return

	def readStatesConfigFile(self, filename):
		"reading the configuration file for alarm_DVR with ConfigParser"
		logging.debug("-==alarm_DVR: readStatesConfigFile(%s)==-", filename)
		configuration = ConfigParser.ConfigParser()
		configuration.read(filename)

		self.hostDVR = configuration.get('GENERAL', 'HOST')
		self.portDVR = configuration.get('GENERAL', 'PORT')
		logging.debug('-==alarm_DVR: readStatesConfigFile(): Host %s Port %d==-', self.hostDVR, self.portDVR)

		logging.debug("-==alarm_DVR: readStatesConfigFile() exit==-")
		return

	def __del__(self):
		"clean up the alarm_DVR on normal exit"
		logging.debug("-==alarm_DVR destructor()==-")
		return

class connectionThreadDVR(threading.Thread):

	def __init__(self, host, port):
		super(connectionThread, self).__init__()
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.bind((host, port))
			self.s.listen(5)
		except socket.error:
			print 'Failed to create socket'
			sys.exit()
		self.clients = []

	def run(self):
		while True:
			conn, address = self.s.accept()
			c = client(conn)
			c.start()
			c.send_msg(u"\r\n")
			self.clients.append(c)
			print '[+] Client connected: {0}'.format(address[0])

def main():
	"main function"
	print "-==alarm_DVR main()==-"
	# Initialize the alarm_DVR class
	dvr = alarm_DVR()

	get_conns = connectionThread(host, port)
	get_conns.start()

	while True:
		try:
			response = raw_input() 
			for c in get_conns.clients:
			c.send_msg(response + u"\r\n")
		except KeyboardInterrupt:
			sys.exit()

	while True:
		time.sleep(1)
	return

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected!"
