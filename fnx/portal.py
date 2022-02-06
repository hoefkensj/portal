#!/usr/bin/env python
import os
import shlex
import subprocess
import time
import timeit
import re
import sys
import termios
import tty
import types
import shutil
debug_slow=0.1



def std_cursorloc():
	buf = ""
	stdin = sys.stdin.fileno()
	tattr = termios.tcgetattr(stdin)
	try:
		tty.setcbreak(stdin, termios.TCSANOW)
		sys.stdout.write("\x1b[6n")
		sys.stdout.flush()
		while True:
			buf += sys.stdin.read(1)
			if buf[-1] == "R":
				break
	finally:
		termios.tcsetattr(stdin, termios.TCSANOW, tattr)
	# reading the actual values, but what if a keystroke appears while reading
	# from stdin? As dirty work around, getpos() returns if this fails: None
	try:
		matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
		groups = matches.groups()
	except AttributeError:
		return None
	return (int(groups[0]), int(groups[1]))

def stdwrite_org_E(ANSI_cursor):
	ansi='\033[{n}E'.format(n=ANSI_cursor)
	def stdout_ansi():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_ansi
def stdwrite_org_F(ANSI_cursor):
	ansi='\033[{n}F'.format(n=ANSI_cursor)
	def stdout_ansi():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_ansi
def stdwrite_org_G(ANSI_cursor):
	ansi='\033[{n}G'.format(n=ANSI_cursor)
	def stdout_ansi():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_ansi
def stdwrite_org_H(ANSI_cursor):
	ansi='\033[{n};{m}H'.format(n=ANSI_cursor[0],m=ANSI_cursor[1])
	def stdout_ansi():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_ansi
def stdwrite_org_K(ANSI_cursor):
	ansi='\033[{n}K'.format(n=ANSI_cursor)
	def stdout_ansi():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_ansi
def stdwrite_string(text, **k):
	def dummy(): pass
	color=k.get('ANSI_Color')
	fn_pre=k.get('pre') if k.get('pre') else [dummy,]
	fn_post=k.get('post') if k.get('post') else [dummy,]
	def stdout_text():
		[pre() for pre in fn_pre]
		sys.stdout.write(text)
		sys.stdout.flush()
		[post()for post in fn_post]
	return stdout_text()

def stdwrite_color(ANSI_color):
	ansi='\033[{}m'.format(ANSI_color)
	def stdout_color():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_color

def ANSI_cursor(F1=1,L1=32,F2=33,L2=64,SO=12,termwidth=64,curs_init_row=3,curs_init_col=1):
	org 								= types.SimpleNamespace()
	org.init						=	stdwrite_org_H([(curs_init_row-3),curs_init_col])
	org.header					=	stdwrite_org_H([(curs_init_row-2),1])
	org.progress				=	stdwrite_org_H([(curs_init_row-1),1])
	# COLS
	org.title_1					=	stdwrite_org_G(F1)
	org.title_1_stat		=	stdwrite_org_G(F1+SO)
	org.title_2					=	stdwrite_org_G(F2)
	org.title_2_stat		=	stdwrite_org_G(F2+SO)
	org.title_2_file		=	stdwrite_org_G(F2+6)
	org.proc						=	stdwrite_org_G(SO)
	org.count						=	stdwrite_org_G(SO+2)
	org.alloc						=	stdwrite_org_E(3)		# ROWS:


	org.clr_left				=	stdwrite_org_K(1)
	org.clr_right				=	stdwrite_org_K(2)
	return org

def ANSI_style():
	clr=types.SimpleNamespace()
	clr.reset			=stdwrite_color('0')
	clr.bold			=stdwrite_color('1')
	clr.ital			=stdwrite_color('2')
	clr.underline	=stdwrite_color('4')
	clr.blink			=stdwrite_color('5')
	clr.inv				=stdwrite_color('7')
	clr.strike		=stdwrite_color('9')
	clr.dunno			=stdwrite_color('9')
	
	clr.noblink		=stdwrite_color('25')
	
	clr.gray			=stdwrite_color('30')
	clr.red				=stdwrite_color('31')
	clr.green			=stdwrite_color('32')
	clr.yellow		=stdwrite_color('33')
	clr.blue			=stdwrite_color('34')
	clr.purple		=stdwrite_color('35')
	clr.bluegreen	=stdwrite_color('36')
	clr.white			=stdwrite_color('37')
	
	return clr


def init_tty():
	try:
		termwidth=shutil.get_terminal_size()[0]
	except Exception as E:
		print(E)




def cpy(src, dst, force=False) -> None:
	"""
	copy progress
	"""
	def cli_count(path):
		org.progress()
		total = [count(len(d) + len(f)) for p,d,f in os.walk(path,topdown=True)]
		return total[-1]-1
	def count(add,tot=[]):
		global debug_slow
		tot += [add]
		stdwrite_string(str(sum(tot)), pre=[org.progress, org.count, clr.red], post=[clr.reset])
		stdwrite_string(']', pre=[clr.reset], post=[clr.reset])
		time.sleep(debug_slow)
		return sum(tot)
	def cp(srcdir, dest) -> None:
		"""
		copys files form srcdir to dest, returns stdout in pipe in realtime
		"""
		cmd = shlex.split(f'cp -rvp {srcdir} {dest}')
		proc_cp = subprocess.Popen(cmd ,stdout=subprocess.PIPE, universal_newlines=True)
		for line in iter(proc_cp.stdout.readline, ''):
			yield line.split('->')[0]#'/'.join(line.split('->')[0].split('/')[len(srcdir.split('/')):])
		proc_cp.stdout.close()
		return_code = proc_cp.wait()
		if return_code:
			raise subprocess.CalledProcessError(return_code, proc_cp)
	def progress(path, tot, cur):
		global debug_slow
		cur= str(cur).zfill(len(str(tot)))
		ppath=format_path(path)
		
		stdwrite_string('Progress: ', pre=[org.progress, clr.bold], post=[clr.reset])
		stdwrite_string('[')
		stdwrite_string(cur, pre=[org.proc, clr.red], post=[clr.reset])
		stdwrite_string('/')
		stdwrite_string(str(tot), pre=[clr.green], post=[clr.reset])
		stdwrite_string(']')
		stdwrite_string('File: ', pre=[org.title_2, clr.bold], post=[clr.reset])
		stdwrite_string(ppath, pre=[org.title_2_file, clr.yellow], post=[clr.reset])
		time.sleep(debug_slow)
		return cur
	def format_path(path):
		termwidth=shutil.get_terminal_size()[0]
		stringwidth=termwidth-38
		if len(path) > (stringwidth-3):
			path=f'...{path[-(stringwidth-6):]}'
			path=path.rjust(stringwidth-6)
		elif len(path) < ((termwidth-16)/2):
			path= path.ljust(termwidth-38)
		return path[:(termwidth-42)]
	print('\n\n')
	org= ANSI_cursor(curs_init_row=std_cursorloc()[0],curs_init_col=std_cursorloc()[1])
	clr= ANSI_style()
	stdwrite_string('PORTAL::' , pre=[org.init,clr.bold, clr.blue], post=[clr.reset])
	stdwrite_string(f'{src}', pre=[clr.ital, clr.yellow], post=[clr.reset])
	stdwrite_string(f'\t>->>\t' , pre=[clr.bold, clr.white], post=[clr.reset])
	stdwrite_string(f'{dst}' , pre=[clr.ital, clr.yellow], post=[clr.reset])
	stdwrite_string('Checking: ', pre=[org.init, org.header, org.title_1, clr.bold], post=[clr.reset])
	stdwrite_string('PENDING', pre=[org.title_1_stat])
	stdwrite_string('Processing: ', pre=[org.title_2, clr.bold], post=[clr.reset])
	stdwrite_string('PENDING', pre=[org.title_2_stat])
	stdwrite_string('Progress: ', pre=[org.progress, clr.bold], )
	stdwrite_string('[', pre=[clr.reset])
	stdwrite_string('0', pre=[org.proc, clr.reset])
	stdwrite_string('/')
	stdwrite_string('0', pre=[org.count])
	stdwrite_string(']', post=[clr.reset])
	stdwrite_string('BUSY'.ljust(11, " "), pre=[org.init, org.header, org.title_1_stat, clr.red, clr.blink], post=[clr.noblink, clr.reset])
	tot=cli_count(path=src)
	stdwrite_string('Done', pre=[org.header, org.title_1_stat, clr.green], post=[clr.reset])
	stdwrite_string('Processing: ', pre=[org.title_2, clr.bold], post=[clr.reset])
	stdwrite_string('BUSY'.ljust(12, " "), pre=[org.title_2_stat, clr.red, clr.blink], post=[clr.noblink, clr.reset])
	start_timer=timeit.default_timer()
	cur=[progress(path,tot,idx) for idx,path in enumerate(cp(src, dst))]
	end_timer=timeit.default_timer()
	stdwrite_string('Done'.ljust(12, " "), pre=[org.header, org.title_2_stat, clr.green], post=[clr.reset])
	stdwrite_string('Finished: ', pre=[org.progress, org.title_2, clr.bold], post=[clr.reset])
	stdwrite_string(f'Copied {tot} Files in {end_timer - start_timer} s', pre=[org.title_2_stat,org.clr_right, clr.blue], post=[clr.reset])
	stdwrite_string('\n\n')



def end(reason='exit'):
	clr= ANSI_style()
	stdwrite_string('ERROR: ', pre=[clr.red, clr.bold, clr.blink], post=[clr.reset])
	stdwrite_string(reason, pre=[clr.red, clr.bold, ], post=[clr.reset])
	print('\n\n')
	exit()

def rmr(path) -> None:
	shutil.rmtree(path)

def link(src,lnk,rel=False) -> None:
	"""
	checks if link location exists and removes anything that is there
	makes symlink lnk --> src
	:param src: source for the link (what the link links to) lnk --> src
	:param lnk: name for the link: mylinkfolder -> ogfolder
	:return: None
	"""
	src=os.path.abspath(src)
	lnk=os.path.abspath(lnk)
	if rel:
		common =len([sf for sf, lf in zip(src.split('/'),lnk.split('/')) if sf == lf ])
		src=f"{'./' if len(lnk.split('/')[common:-1])<1 else ''}{'/'.join(['..' for folder in lnk.split('/')[common:-1]]+src.split('/')[common:-1]+[os.path.split(src)[1]])}"
	os.symlink(src,lnk)

def portal(src, dst, rel=False) -> None:
	dst=os.path.abspath(os.path.realpath(os.path.expanduser(os.path.expandvars(dst)))) #a(bsolute)r(eal)_dst
	src=os.path.abspath(os.path.realpath(os.path.expanduser(os.path.expandvars(src))))
	fulldst=os.path.join(dst,os.path.basename(src))
	if os.path.abspath(dst) == os.path.abspath(src):
		end(reason=f'ERROR source({src}) and destination({dst}) are the same or nested')
	if not os.path.exists(dst)	:
		os.makedirs(dst)
	
	cpy(src,fulldst)
	
	os.renames(src,os.path.join(os.path.dirname(src),f'{os.path.basename(src)}.backup001'))
	link(fulldst,src)
	#rmr(src)

# portal('~/ikkel/', '/home/hoefkens/tmp2copy')
portal('/home/hoefkens/testdir' ,'~/1111cptestdir/')




