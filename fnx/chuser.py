#!/usr/bin/env python
import os
import sys
import subprocess
import shlex
import base64


from subprocess import Popen, PIPE

def check_polkit():
		return '/usr/bin/env pkexec' if os.path.exists('/usr/bin/pkexec') else '/usr/bin/env bash sudo -A'
	
def getroot():
		helper= check_polkit()
		sudo_password = env_passwd()
		
		args = ['sudo', sys.executable] + sys.argv + [os.environ]
		proc = subprocess.Popen(f'echo "{sudo_password}" |sudo -S python old/portal.py',shell=True, universal_newlines=True,stdout=subprocess
		.PIPE)
		print(proc)

		os.execlpe('sudo', *args)
		return
		
def ask_passwd():
	cmd='zenity --password --title="Enter your ROOT or SUDO password:" --timeout=0'
	password=subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True).stdout
	passbytes = password.encode('ascii')
	b64_bytes = base64.b64encode(passbytes)
	b64_pass = b64_bytes.decode('ascii')
	os.environ['PORTAL_STORE']=b64_pass
	return password

def env_passwd():
	base64_message = os.environ.get('PORTAL_STORE')
	base64_bytes = base64_message.encode('ascii')
	message_bytes = base64.b64decode(base64_bytes)
	passw = message_bytes.decode('ascii')
	return passw
	
 

print(ask_passwd())
print(env_passwd())


if not os.geteuid()==0:
	getroot()

# print(getroot('pkexec'))
# print(os.geteuid)