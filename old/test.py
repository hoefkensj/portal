#!/usr/bin/env python

import os,sys,shlex,shutil
import subprocess
import multiprocessing
import time
import timeit
import functools
timer = timeit.default_timer

def std_cursor(lines=[]):
	proc=subprocess.Popen('printf "\033[6n"',	stdout=subprocess.PIPE,	universal_newlines=True,shell=True)
	stat=proc.poll()
	while stat is None:
		lines+=[proc.stdout.readline()]
		stat=proc.poll()		
	lines+=proc.stdout.readlines()
	return lines

cursor=std_cursor()
for line in cursor:
    print('\n\n\n\n')
    print(line)
    print('\n\n\n\n')
    
	
