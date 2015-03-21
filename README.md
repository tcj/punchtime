# punchtime
Time clock daemon in client/server Python fashion

<H5>punchtimed.py</H5> 
<H6>(daemon)</H6>
  intended to be run as timeclock user (or similar)

  writes out log files intended to be writable only by timeclock user and superuser

  receives signal SIGUSR2 to read punch file 
  
<H5>punchtime.py</H5> 
<H6>(client)</H6>
  run as client user

  punch in ( -i )   or out ( -o )

  writes to "punch" file in /tmp, signals daemon to read it

<h6>punch files</h6>
  punch file contains uid, username, type of event (out or in)

daemon determines actual uid and date/time from statting the punchfile

once client/server communication is complete, punch file is removed (by client)

log files of punch events are kept in /tmp but this will be configurable
