#!/usr/bin/python

# punchtime
# time punch client

import posix
import signal

def get_daemon_pid():
	try:
		pidfile = file('/tmp/punchtime.pid','r')
	except:
		print "no pid file.  is daemon running?"
		exit(1)
		
	pid = int(pidfile.readline())
	pidfile.close()
	return pid	
	
if __name__ == '__main__':
	daemon_pid = get_daemon_pid()
	print get_daemon_pid()
	posix.kill(daemon_pid,signal.SIGUSR2)
	