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

def init_tty():
	try:
		termwidth=shutil.get_terminal_size()[0]
	except Exception as E:
		print(E)

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

def ANSI_fn(fn,ESC='\033'):
	def ansi(SEQ):
		return str_ANSI(ESC=ESC,SEQ=SEQ,FN=fn)
	return ansi
	
def str_ANSI(ESC='\033',SEQ='{SEQ}',FN='{FN}'):
	return '{ESC}[{SEQ}{FN}'.format(ESC=ESC,SEQ=SEQ,FN=FN)
	
ANSI_E= ANSI_fn('E')
ANSI_F= ANSI_fn('F')
ANSI_G= ANSI_fn('G')
ANSI_H= ANSI_fn('H')
ANSI_K= ANSI_fn('K')
ANSI_m= ANSI_fn('m')

def ANSI_style(style):
	STYLES= {
	'reset'			: 	0,
	'bold'			: 	1,
	'ital'			: 	2,
	'line'			: 	4,
	'blink'			: 	5,
	'inv'				: 	7,
	'strike'		: 	9,
	'noblink'		:		25,
	'gray'			:		30,
	'red'				:		31,
	'green'			:		32,
	'yellow'		:		33,
	'blue'			:		34,
	'purple'		:		35,
	'bluegreen'	:		36,
	'white'			:		37,
		}
	return ANSI_m(STYLES.get(style))

def txt_markup(**k):
	markup=[ANSI_style(style) for style in k.get('m') if k.get('m')]
	reset=ANSI_style('reset') if k.get('text')[-7:] != ANSI_style('reset') else ''
	return '{markup}{text}{reset}'.format(markup=str().join(markup),text=k.get('text'),reset=str().join(reset))

def stdout_settxt(*a,**k):
	text= k.get('txt') if k.get('txt') else str().join(a) if a else ''
	styles=[style for style in k.get('style') if k.get('style')]
	txt_styled=txt_markup(text=text,m=styles)
	def stdout_text():
		return str(txt_styled)
	return stdout_text()

def setstyle(**k):
	text='{placeholder}'
	styles=[style for style in k.get('style') if k.get('style')]
	txt_styled=txt_markup(text=text,m=styles)
	def stdout_text(text):
		return str(txt_styled.format(placeholder=text))
	return stdout_text

def style(*a,**k):
 return txt_markup(text=k.get('txt') or a[0],m=k.get('style'))
	
def TERM_init(**k):
	ALLOC=k.get('allocate')
	COLW=k.get('colw')
	def init_term():
		try:
			termwidth=shutil.get_terminal_size()[0]
			termheight=shutil.get_terminal_size()[1]
		except Exception as E:
			print(E)
		finally:
			return termwidth,termheight
	def update_term():
			return shutil.get_terminal_size()[0],shutil.get_terminal_size()[1]
	def allocate(ALLOC):
		width=init_term()[0]
		print('\n\n\n')
		return std_cursorloc()
	def segment():
		SEG={}
		curs_loc=allocate(ALLOC)
		SEG['top'] = ANSI_H(f'{(curs_loc[0]-ALLOC)};0')
		SEG['sec'] = ANSI_H(f'{(curs_loc[0]-(ALLOC-1))};0')
		SEG['bot'] = ANSI_H(f'{(curs_loc[0])};0')
		SEG['c11'] = ANSI_G(0)
		SEG['c21'] = ANSI_G(COLW+1)
		SEG['c12'] = ANSI_G(divmod(COLW,2)[0]+1)
		SEG['c22'] = ANSI_G(((COLW+1)+divmod(COLW,2)[0]+1))
		return SEG
	return segment

def org(loc,ALLOC=4,colw=24,termwidth=64):
	TERM=TERM_init(allocate=ALLOC,colw=colw)
	ORG= TERM()
	orgs={
	'init'				:	f"{ORG['top']}" ,
	'header'			:	f"{ORG['sec']}" ,
	'progress'		:	f"{ORG['bot']}" ,
	
	'tit1'				:	f"{ORG['sec']}{ORG['c11']}" ,
	'tit1_stat'		:	f"{ORG['sec']}{ORG['c12']}" ,
	'tit2'				:	f"{ORG['sec']}{ORG['c21']}" ,
	'tit2_stat'		:	f"{ORG['sec']}{ORG['c22']}" ,
	'prog'				:	f"{ORG['bot']}{ORG['c11']}{ANSI_G(2)}",
	'count'				:	f"{ORG['bot']}{ORG['c11']}{ANSI_G(4)}" ,
	
	'proc'				:	f"{ORG['bot']}{ORG['c21']}",
	'proc_file'		:	f"{ORG['bot']}{ORG['c22']}",

	'clr_left'		:	ANSI_K(1),
	'clr_right'		:	ANSI_K(2),
	}
	return orgs.get(loc)

def stdout_write(*a,**k):
	def write(*a,**k):
		sys.stdout.write(org(str(k.get('org'))))
		sys.stdout.write(style(*a,**k))
		sys.stdout.write(ANSI_style('reset'))
		sys.stdout.flush()
	return write
# txt_test=stdout_settxt('test',style=['blue','line'])
# print(txt_test)                               stdout_write=stdout_write()

# print(DONE)
# style('test3',style=['yellow','blink'])
def preset():
	mem= types.SimpleNamespace()
	style_green=setstyle(style=['green'])
	style_blue=setstyle(style=['blue'])
	style_blue=setstyle(style=['red'])
	style_bold=setstyle(style=['bold'])
	style_line=setstyle(style=['line'])
	style_blink=setstyle(style=['blink'])
	# txt_test\
	mem.DONE=style_green('DONE')
	mem.BUSY=style_blink(style_green('BUSY'))
	mem.CHECK=style_bold('Checking :')
	mem.PROC=style_bold('Processing :')
	# stdout_write(txt='test', style=['red','line'], org='tit2')
	return mem
stdout_write=stdout_write()
def cpy(src, dst, force=False) -> None:
	"""
	copy progress
	"""
	global stdout_write
	mem=preset()

	print('\n\n')

	stdout_write(txt='PORTAL::' , 								org='init',										style=['bold','blue'], 										)
	stdout_write(txt='{src}'.format(src=src), 																	style=['ital','yellow'], 									)
	stdout_write(txt='\t>->>\t' , 																							style=['bold','white'], 										)
	stdout_write(txt='{dst}'.format(dst=dst) , 																	style=['ital','yellow'],										)
	stdout_write(txt='Checking: ', 								org='tit1',										style=['bold',],														)
	stdout_write(txt='PENDING', 									org='tit1_stat',																													)
	stdout_write(txt='Processing: ', 							org='tit2',										style=['bold'],)
	stdout_write(txt='PENDING', 									org='tit2_stat'	,																													)
	stdout_write(txt='Progress: ',								org='progress',								style=['bold'], )
	stdout_write(txt='[',)
	stdout_write(txt='0', 												org='proc')
	stdout_write(txt='/')
	stdout_write(txt='0', 												org='count',)
	stdout_write(txt=']',)
	stdout_write(txt='BUSY'.ljust(11," "), 				org='tit1_stat',							style=['red',' blink'], )
	tot=cli_count(org, count, path=src)
	stdout_write(txt='Done', 													org='tit1_stat',							style=['green'],)
	stdout_write(txt='Processing: ', 									org='tit2',										style=['bold'], )
	stdout_write(txt='BUSY'.ljust(12, " "), 					org='tit2_stat',							style=['red',' blink'],)
	start_timer=timeit.default_timer()
	cur=[progress(org, style, path, tot, idx) for idx, path in enumerate(cp(src, dst))]
	end_timer=timeit.default_timer()
	stdout_write(txt='Done'.ljust(12, " "), style=['org.header',' tit2_stat, green'], )
	stdout_write(txt='Finished: ', style=['org.progress',' tit2, bold'], )
	stdout_write(txt=f'Copied {tot} Files in {end_timer - start_timer} s', style=['tit2_stat','org.right, blue'], )
	stdout_write('\n\n')

def progress(org, clr, path, tot, cur):
	global debug_slow
	cur= str(cur).zfill(len(str(tot)))
	ppath=format_path(path)
	
	stdout_write(txt='Progress: ', pre=[org.progress, clr.bold], post=[clr.reset])
	stdout_write(txt='[')
	stdout_write(cur, pre=[org.proc, clr.red], post=[clr.reset])
	stdout_write(txt='/')
	stdout_write(txt=str(tot), pre=[clr.green], post=[clr.reset])
	stdout_write(txt=']')
	stdout_write(txt='File: ', pre=[tit2, clr.bold], post=[clr.reset])
	stdout_write(ppath, pre=[tit2_file, clr.yellow], post=[clr.reset])
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

def count(org, clr, add, tot=[]):
	global debug_slow
	tot += [add]
	stdwrite_string(str(sum(tot)), pre=[org.progress, org.count, clr.red], post=[clr.reset])
	stdwrite_string(']', pre=[clr.reset], post=[clr.reset])
	time.sleep(debug_slow)
	return sum(tot)

def cli_count(org, count, path):
	org.progress()
	total = [count(len(d) + len(f)) for p,d,f in os.walk(path,topdown=True)]
	return total[-1]-1

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




