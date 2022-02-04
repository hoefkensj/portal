#!/usr/bin/env python
#[DOCS]
'''	'''
#[CODE]
import os
import shlex
import shutil
import subprocess
import sys
import time
import timeit



def proc_copy(src,dst):
	#test src to be file or folder or link
	#abort if is link TODO:	choice -to copy link , and link to the link leaving the "data" untouched
	#abort if is link TODO:	choice -to copy data , and changing the link so that it points to the new data location
	
	#if dir : the last part si the "name"  then unless  --rename is used
	# /test/ikkel/[data]  /new/ => creates /new/ikkel/[data]  -
	# with --rename  /test/ikkel /new/ => creates /new/[data]
	# if dst does not exist create it , (mkdir-p)
	
	def  dir_src(src):
		src_islink=os.path.islink(src)
		if not src_islink:
			src=os.path.abspath(os.path.realpath(src))
			dir_srctocopy=os.path.split(src)[1]
			
	def dst_exist(dst):
		#test if destination exists
		dst_exists=os.path.exists(dst)
		if not dst_exists:
			os.makedirs(dst)
			dst_exist(dst)
		else:
			dst_islink=os.path.islink(dst)
			if not dst_islink:
				dst=os.path.abspath(os.path.realpath(dst))
		dir_dsttocopy=os.path.join(dst,os.path.split(os.path.abspath(os.path.realpath(src)))[1])
		dst_dirtocopy_exists= os.path.exists(dir_dsttocopy)
		if not dst_dirtocopy_exists:
			pass

def cp(src, dst,f='',df='av') -> None:
	"""
	Copies files form srcdir to dest, returns stdout in pipe in realtime
	"""
	flags=df+f
	command_cp=f'cp -{flags} {src} {dst}'
	args=shlex.split(command_cp)
	proc_cp = subprocess.Popen(args , stdout=subprocess.PIPE, universal_newlines=True)
	for line in iter(proc_cp.stdout.readline, ''):
		yield '/'.join(line.split('->')[0].split('/')[len(src.split('/')):])
	proc_cp.stdout.close()
	return_code = proc_cp.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code, cp)

def cpy_api(dir_src, dir_dst) -> None:
	"""
	copy progress
	"""
	#copy = robocopy if os.name == 'NT' else cp
	
	# sys.stdout.write('\u001b[38;5;123mChecking\u001b[0m/:\033[1E[0/0]')
	
	total = [count_depr(pdf) for pdf in os.walk(dir_src, topdown=True)]
	# sys.stdout.write('\033[1FChecking: Done ; \u001b[38;5;123mCopying:\u001b[0m\033[1E[')
	# start_timer=timeit.default_timer()
	
	proc_copy(dir_src, dir_dst)

def cpy_cli(src, dst)->None:
	"""
	copy progress
	"""
	

	total= counter_cli(src, cli=True)
	sys.stdout.write(' \033[38;5;123mCopying:\033[0m\033[1E[')
	start_timer=timeit.default_timer()
	cur=[progress_cli(line, sum(total), idx) for idx, line in enumerate(copy(src, dst))]
	end_timer=timeit.default_timer()

def closure_walk(path):
	"""

	:param path:
	:return:
	"""
	def walk():
		return os.walk(path, topdown=True)
	return walk

def total_count(sub_totals=[],**k) -> int:
	"""

	:param sub_totals:
	:param k:
	:return:
	"""
	sub_totals+=[k.get('add')]
	return sum(sub_totals)

def updtotal_cli(run_total):
	return sys.stdout.write(f'\033[G\033[38;5;123m{run_total}\u001b[0m')


def counter_api(src_walk):
		return ((len(d)+len(f)) for p,d,f in src_walk())

def counter_cli(src_walk):
		total=[updtotal_cli(cur) for cur in ((len(d)+len(f)) for p,d,f in src_walk())]
		return total


def count_depr(pdf, tot=[]):
	tot += [(len(pdf[1]) + len(pdf[2]))]
	sys.stdout.write(f'\033[4G\u001b[38;5;123m{sum(tot)}\u001b[0m]')
	# print(f'returning:{ sum(tot)} ')
	return sum(tot)

def format_copy_line(line):
	termwidth=shutil.get_terminal_size()[0]
	if line[(termwidth-4):]:
		line = f'{line[:termwidth-4]}...'
	return line

def clo_wr(string):
	def write():
		return sys.stdout.write(string)
	return write

def progress_static_cli(tot):
	len_tot=len(str(tot))
	sys.stdout.write('Checking :\x1b[32m Done\x1b[0m # Process\x1b[5m :\x1b[0m')
	sys.stdout.flush()
	sys.stdout.write('\n[')
	sys.stdout.write('0'.zfill(len_tot))
	sys.stdout.write('\033[0m/')
	sys.stdout.write(str(tot))
	sys.stdout.write(']\n')

def progress_dynamic_cli(line, tot, cur):
	len_tot=len(f'{tot}')#3= [
	str_cur= f'{cur}'

	loc_0=clo_wr('\x1b[1E')
	loc_1=clo_wr('\033[1F\033[2G')
	loc_end=clo_wr('\033[2E\033[1G')								#x=2
	col_1=clo_wr('\033[38;5;123m')
	col_reset=clo_wr('\033[0m')
	sep=clo_wr('/')
	
	
	loc_0()
	progress_static_cli(tot)
	loc_1()
	sys.stdout.write(f'{col_1()}----')
	col_reset()
	loc_1()
	


	sys.stdout.write(format_copy_line(str(line)))
	loc_end()
	return cur

# str_stdout_checking='Checking:'
# str_stdout_done= '\033[1m\033[32m' +'Done' + '\033[0m'

walk=closure_walk('/etc')
total=counter_cli([updtotal_cli(cur) for cur in ((len(d)+len(f)) for p,d,f in walk())])
print(f'\n {total}')