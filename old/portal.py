#!/usr/bin/env python
import os,sys,shlex,shutil
import subprocess
import multiprocessing
import time
import timeit
import functools
import termios
import tty
import re
import types

debug_slow=1
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


def stdwrite_org(ansi):
	def stdout_ansi():
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


def sns_org(**k):
	def defaults():
			k['DEFAULT'] = {'t1': 1, 't2': 24, 'ts': 12}
			k['t1'] = k.get('t1') or k['DEFAULT'].get('t1')
			k['t2'] = k.get('t2') or k['DEFAULT'].get('t2')
			k['ts'] = k.get('ts') or k['DEFAULT'].get('ts')
	defaults()
	org = types.SimpleNamespace()
	curs_init_row=std_cursorloc()[0]
	curs_init_col=std_cursorloc()[1]
	org.init						=	stdwrite_org('\033[{n};{m}H'.format(n=(curs_init_row-2),m=curs_init_col))
	# ROWS:
	org.header					=	stdwrite_org('\033[{};1H'.format(curs_init_row-2))
	org.progress				=	stdwrite_org('\033[{};1H'.format((curs_init_row-1)))
	# COLS
	org.title_1					=	stdwrite_org('\033[{}G'.format(k.get('t1')))
	org.title_1_stat		=	stdwrite_org('\033[{}G'.format(k.get('t1')+k.get('ts')))
	org.title_2					=	stdwrite_org('\033[{}G'.format(k.get('t2')))
	org.title_2_stat		=	stdwrite_org('\033[{}G'.format(k.get('t2')+k.get('ts')))
	org.proc						=	stdwrite_org('\033[{}G'.format(k.get('ts')))
	org.count						=	stdwrite_org('\033[{}G'.format(2+k.get('ts')))
	return org

def sns_clr():
	clr=types.SimpleNamespace()
	clr.blink=stdwrite_color('5')
	clr.noblink=stdwrite_color('25')
	clr.gray=stdwrite_color('30')
	clr.red=stdwrite_color('31')#38;5;14
	clr.green=stdwrite_color('32')
	clr.yellow=stdwrite_color('33')
	clr.blue=stdwrite_color('34')

	clr.reset=stdwrite_color('0')
	clr.bold=stdwrite_color('1')
	clr.ital=stdwrite_color('2')
	clr.underline=stdwrite_color('4')
	clr.inv=stdwrite_color('7')
	clr.strike=stdwrite_color('9')
	clr.dunno=stdwrite_color('9')
	
	return clr

timer = timeit.default_timer
print('\n')
# curs_init_row=std_cursorloc()[0]
# curs_init_col=std_cursorloc()[1]

org=sns_org()
clr=sns_clr()



def cli_init():
	stdwrite_string('Checking: ',pre=[org.init,	org.header,	org.title_1,clr.bold],post=[clr.reset])
	stdwrite_string('PENDING',pre=[org.title_1_stat])
	stdwrite_string('Processing: ',pre=[org.title_2,clr.bold],post=[clr.reset])
	stdwrite_string('PENDING',pre=[org.title_2_stat])
	stdwrite_string('Progress: ',pre=[org.progress,clr.bold],)
	stdwrite_string('[',pre=[clr.reset])
	stdwrite_string('0',pre=[org.proc,clr.reset])
	stdwrite_string('/')
	stdwrite_string('0',pre=[org.count])
	stdwrite_string(']',post=[clr.reset])

def count(add,tot=[]):
	global debug_slow
	tot += [add]
	stdwrite_string(str(sum(tot)),pre=[org.progress,org.count,clr.red],post=[clr.reset])
	stdwrite_string(']',pre=[clr.reset],post=[clr.reset])
	time.sleep(debug_slow)
	return sum(tot)

def cli_count(path="."):
	org.progress()
	total = [count(len(d) + len(f)) for p,d,f in os.walk(path,topdown=True)]
	return total[-1]-1

def cpy(srcdir, dest,force=False) -> None:
	"""
	copy progress
	"""
	stdwrite_string('Checking: '					,pre=[org.init,	org.header,	org.title_1,clr.bold],post=[clr.reset])
	stdwrite_string('PENDING'							,pre=[org.title_1_stat])
	stdwrite_string('Processing: '				,pre=[org.title_2,clr.bold],post=[clr.reset])
	stdwrite_string('PENDING'							,pre=[org.title_2_stat])
	stdwrite_string('Progress: '					,pre=[org.progress,clr.bold],)
	stdwrite_string('['										,pre=[clr.reset])
	stdwrite_string('0'										,pre=[org.proc,clr.reset])
	stdwrite_string('/')
	stdwrite_string('0'										,pre=[org.count])
	stdwrite_string(']'										,post=[clr.reset])
	stdwrite_string('BUSY'.ljust(11," ")	,pre=[org.init,org.header,org.title_1_stat,clr.red,clr.blink],post=[clr.noblink,clr.reset])
	tot=cli_count(path=srcdir)
	stdwrite_string('Done',pre=[org.header,	org.title_1_stat,	clr.green],post=[clr.reset])
	stdwrite_string('Processing: ',pre=[org.title_2,clr.bold],post=[clr.reset])
	stdwrite_string('BUSY'.ljust(12," "),pre=[org.title_2_stat,	clr.red,	clr.blink],post=[clr.noblink,	clr.reset])
	org.path=stdwrite_org('\033[{n}G'.format(n=((len(str(tot))*2)+36)))
	start_timer=timer()
	cur=[progress(path,tot,idx,org.path) for idx,path in enumerate(cp(srcdir, dest))]
	end_timer=timer()
	org.header()
	org.title_2_stat()
	clr.green()
	stdwrite_string('Done'.ljust(12," "))
	clr.reset()
	stdwrite_string('Finished: ',pre=[org.progress,org.title_2,clr.bold],post=[clr.reset])
	stdwrite_string(f'Copied {tot} Files in {end_timer-start_timer} s',pre=[org.title_2_stat,clr.blue],post=[clr.reset])
	stdwrite_string('\n\n')




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

def progress(path, tot, cur,loc):
	global debug_slow
	cur= str(cur).zfill(len(str(tot)))
	
	def format_path(path):
		termwidth=shutil.get_terminal_size()[0]
		stringwidth=termwidth-(36+(2*len(str(tot))))
		if len(path) > (stringwidth-3):
			path=f'...{path[-(stringwidth-6):]}'
		return path.rjust(stringwidth-6)
		
	ppath=format_path(path)
	stdwrite_string('Progress: ',pre=[org.progress,clr.bold],post=[clr.reset])
	stdwrite_string('[')
	stdwrite_string(cur,pre=[org.proc,clr.green],post=[clr.reset])
	stdwrite_string('/')
	stdwrite_string(str(tot),pre=[clr.green],post=[clr.reset])
	stdwrite_string(']')
	stdwrite_string('File: ',pre=[org.title_2,clr.bold],post=[clr.reset])
	stdwrite_string(ppath,pre=[org.title_2_stat,clr.blue],post=[clr.reset])
	time.sleep(debug_slow)
	return cur

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

def portal(src, dst, method, force, rel) -> None:
	ar_dst=os.path.abspath(os.path.realpath(dst)) #a(bsolute)r(eal)_dst
	if os.path.islink(src):
		end(reason=f'ERROR: source ({src}) is a link')
	if os.path.abspath(dst) == os.path.abspath(src):
		end(reason=f'ERROR source({src}) and destination({dst}) are the same')
	copy=(force(cpy, src, dst) if force else end(reason=f'ERROR {os.path.abspath(dst)} exists (use --force to overwrite)')) if os.path.exists(dst)	else cpy
	methods={
		'bind' : bind,
		'link'	: link,
		}
	method=methods[method]
	copy(src,dst)
	rmr(src)
	method(dst,src,rel)



cpy('/home/hoefkens/tmp/', '/home/hoefkens/tmpcopy/')





