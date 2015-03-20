#!/usr/bin/python

# Time punch daemon
# Listens for signal and punches a user in when signal received
# Signal used: SIGUSR2

import glob
import os
import posix
import signal
import time

def ingest_timepunch():
	# stat the UID from the file
	# stat other things as well (time)
	pass
	
	
def usr2_received(signal, frame):
	print "Signal received"
	

if __name__ == '__main__':
	# TODO: don't run again if pid file exists
	
	my_pid = posix.getpid()
	try:
		pid_file = file('/tmp/punchtime.pid','w')
	except: 
		print "couldn't open pid file.  aborting"
		exit(1)
		
	pid_file.write(str(my_pid))
	pid_file.close()
	
	done = False
	signal.signal(signal.SIGUSR2, usr2_received)
	while not done:
		signal.pause()
	
	os.remove(pid_file)
	
