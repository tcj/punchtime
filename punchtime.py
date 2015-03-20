#!/usr/bin/python

# punchtime
# time punch client

import os
import posix
import signal

def write_flag_file(flag_file):
	uid = posix.getuid()
	username = posix.getlogin()
	
	try: 
		flagfile = file(flag_file,'w')
	except:
		print "cannot open flag file, exiting"
		exit(1)
		
	flagfile.write("%d %s" % (uid, username))
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

	
if __name__ == '__main__':
	mypid = posix.getpid()	
	flag_file = '/tmp/punch.%s' % str(mypid)
	
	daemon_pid = get_daemon_pid()
	print get_daemon_pid()
	write_flag_file(flag_file)
	posix.kill(daemon_pid,signal.SIGUSR2)
	# TODO: clear flag file even if signal fails
	clear_flag_file(flag_file)

