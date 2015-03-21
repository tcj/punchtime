# punchtime
Time clock daemon in client/server Python fashion

punchtimed.py :    (daemon)
  intended to be run as timeclock user (or similar)
  writes out log files intended to be writable only by timeclock user and superuser
  receives signal SIGUSR2 to read punch file 
  
punchtime.py :     (client)
  run as client user
  punch in ( -i )   or out ( -o )
  writes to "punch" file in /tmp, signals daemon to read it
  
punch file contains uid, username
daemon determines actual uid and date/time from statting the punchfile

once client/server communication is complete, punch file is removed (by client)
log files of punch events are kept in /tmp but this will be configurable
