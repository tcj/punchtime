#!/usr/bin/python

# Time punch daemon
# Listens for signal and punches a user in when signal received
# Signal used: SIGUSR2

import glob
import os
import posix
import signal
import time

try: 
	import json
except ImportError:
	import simplejson as json


# configure: path for punch files  (default: /tmp)
# configure: path for database


def write_to_punch_log(punch_event):
	today = time.localtime(time.time())[0:3]
	logname = "punchtime-%d-%d-%d.log" % today

	try:
		logfile = file('/tmp/%s' % logname,'a')
	except:
		print "log file inaccessible"
		exit(1)
	logfile.write(json.dumps(punch_event))
	logfile.write("\n")
	logfile.close()
		
def ingest_timepunch():
	# stat the UID from the file
	# stat other things as well (time)
	punches = glob.glob('/tmp/punch.*')
	for punch in punches:
		client_pid = int(punch.split('.')[1].strip())
		print 'client PID = %s' % client_pid
		try: 
			punch_file = file(punch,'r')
		except:
			"can't read punch file %s" % punch
		else:
			punchstat = os.stat(punch)
			print "file stats: uid %d, ctime %s, localtime %s" % \
				(punchstat.st_uid, punchstat.st_ctime, time.localtime(punchstat.st_ctime))
			uid, user, event_type = punch_file.readline().split(' ')
			print "punch %s user #%s, %s." % (event_type, uid, user)
			punch_file.close()
			# Signal client we've read the file
			try:
				os.kill(int(client_pid), signal.SIGUSR1)
			except:
				print "pid %d not found" % client_pid
			
			punch_event = (punchstat.st_uid, punchstat.st_ctime, uid, user, event_type)
			write_to_punch_log(punch_event)


def usr2_received(signal, frame):
	print "Signal received, ingesting time punch"
	ingest_timepunch()

def clean_up_punches():
	punches = glob.glob('/tmp/punch.*')
	for punch in punches:
		os.remove(punch)


if __name__ == '__main__':
	# TODO: don't run again if pid file exists
	
	# Remove stale punches 
	clean_up_punches()
	
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
	
