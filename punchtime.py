#!/usr/bin/python

# punchtime
# time punch client

import os
import posix
import signal
import sys
import time

acknowledged = False

def write_flag_file(flag_file, event_type):
	uid = posix.getuid()
	username = posix.getlogin()
	
	try: 
		flagfile = file(flag_file,'w')
	except:
		print "cannot open flag file, exiting"
		exit(1)
		
	flagfile.write("%d %s %s" % (uid, username, event_type))
	flagfile.close()
	
def clear_flag_file(flag_file):
	if os.path.exists(flag_file):
		os.remove(flag_file)


def get_daemon_pid():
	try:
		pidfile = file('/tmp/punchtime.pid','r')
	except:
		print "no pid file.  is daemon running?"
		exit(1)
		
	pid = int(pidfile.readline())
	pidfile.close()
	return pid	

def handle_signal(num, thread):
	global acknowledged
	if num == signal.SIGUSR1:
		print "acknowledgment received."
		acknowledged = True

	
if __name__ == '__main__':
	usage = """
Usage: %s	
	-i     punch in
	-o     punch out
""" % sys.argv[0]

	if (len(sys.argv) < 2) or (sys.argv[1] not in ['-i','-o']) :
		print usage
		exit(1)

	event_type = "in" if sys.argv[1]=="-i" else "out"

	mypid = posix.getpid()	
	daemon_pid = get_daemon_pid()
	print "my pid = %d, daemon_pid = %d" % (mypid, daemon_pid)

	signal.signal(signal.SIGUSR1, handle_signal)

	flag_file = '/tmp/punch.%s' % str(mypid)	
	write_flag_file(flag_file, event_type)

	# Signal daemon that our punch is ready
	posix.kill(daemon_pid,signal.SIGUSR2)
	
	# Wait for acknowledgment
	while not acknowledged:
		signal.pause()
	
	clear_flag_file(flag_file)
	
	# TODO: clear flag file even if signal fails?


