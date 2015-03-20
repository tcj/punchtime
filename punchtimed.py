#!/usr/bin/python

# Time punch daemon
# Listens for signal and punches a user in when signal received
# Signal used: SIGUSR2

import signal

def usr2_received(signal, frame):
	print "Signal received"
	

if __name__ == '__main__':
	signal.signal(signal.SIGUSR2, usr2_received)
	signal.pause()
	
