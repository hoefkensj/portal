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

print("\n")
timer = timeit.default_timer
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
	color=k.get('ANSI_Color')
	def stdout_text():
		sys.stdout.write(text)
		sys.stdout.flush()
	return stdout_text()
def stdwrite_color(ANSI_color):
	ansi='\033[{}m'.format(ANSI_color)
	def stdout_color():
		sys.stdout.flush()
		sys.stdout.write(ansi)
		sys.stdout.flush()
	return stdout_color

curs_init_row=std_cursorloc()[0]-2
curs_init_col=std_cursorloc()[1]

org_init=stdwrite_org('\033[{n};{m}H'.format(n=curs_init_row,m=curs_init_col))
org_startprogress=stdwrite_org('\033[2E\033[2G')
org_count=stdwrite_org('\033[4G')
org_header=stdwrite_org('\033[{};1H'.format(curs_init_row))
org_progress=stdwrite_org('\033[{};1H'.format(curs_init_row+1))
org_title_1=stdwrite_org('\033[1G')
org_title_2=stdwrite_org('\033[24G')
org_title_1_stat=stdwrite_org('\033[{}G'.format(1+11))
org_title_2_stat=stdwrite_org('\033[{}G'.format(24+12))

col_blink=stdwrite_color('5')
col_noblink=stdwrite_color('25')
col_green=stdwrite_color('32')
col_active=stdwrite_color('31')#38;5;14
col_reset=stdwrite_color('0')
col_bold=stdwrite_color('1')

def cli_init():

	org_init()
	org_header()
	org_title_1()
	col_bold()
	stdwrite_string('Checking: ')
	col_reset()
	stdwrite_string(' ')
	stdwrite_string('PENDING')
	stdwrite_string('    ')
	col_bold()
	stdwrite_string('Processing: ')
	col_reset()
	stdwrite_string('PENDING')
	org_progress()
	stdwrite_string('[')
	col_bold()
	stdwrite_string('0')
	col_reset()
	stdwrite_string('/')
	col_bold()
	stdwrite_string('0')
	col_reset()
	stdwrite_string(']')

def cli_start():
	org_init()
	org_header()
	org_title_1_stat()
	col_active()
	col_blink()
	stdwrite_string('BUSY'.ljust(12," "))
	col_noblink()
	col_reset()

def count(add,tot=[]):
	tot += [add]
	org_progress()
	org_count()
	col_active()
	sys.stdout.write(str(sum(tot)))
	col_reset()
	stdwrite_string(']')
	time.sleep(0.01 )
	return sum(tot)

def cli_count(path="."):
	total = [count(len(d) + len(f)) for p,d,f in os.walk(path,topdown=True)]
	return total[-1]-1

def cli_count_done():
	org_header()
	org_title_1_stat()
	col_green()
	stdwrite_string('Done        ')
	col_reset()
	org_title_2()
	col_bold()
	stdwrite_string('Processing: ')
	col_reset()
	org_title_2_stat()
	col_active()
	col_blink()
	stdwrite_string('BUSY'.rjust(12," "))
	col_noblink()
	col_reset()

def cpy(srcdir, dest,force=False) -> None:
	"""
	copy progress
	"""
	cli_init()
	cli_start()
	tot=cli_count(path=srcdir)
	cli_count_done()
	org_path=stdwrite_org('\033[{n}G'.format(n=((len(str(tot))*2)+6)))
	start_timer=timer()
	cur=[progress(path,tot,idx,org_path) for idx,path in enumerate(cp(srcdir, dest))]
	end_timer=timer()
	org_header()
	org_title_2_stat()
	col_green()
	stdwrite_string('Done'.ljust(12," "))
	col_reset()
	stdwrite_string('\n\n')

def cp(srcdir, dest) -> None:
	"""
	copys files form srcdir to dest, returns stdout in pipe in realtime
	"""
	cmd = shlex.split(f'cp -rvp {srcdir} {dest}')
	proc_cp = subprocess.Popen(cmd ,stdout=subprocess.PIPE, universal_newlines=True)
	for line in iter(proc_cp.stdout.readline, ''):
		yield '/'.join(line.split('->')[0].split('/')[len(srcdir.split('/')):])
	proc_cp.stdout.close()
	return_code = proc_cp.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code, cp)

def progress(path, tot, cur,loc):
	cur= str(cur).zfill(len(str(tot)))
	
	def format_path(path):
		termwidth=shutil.get_terminal_size()[0]
		part1=(2*len(str(tot)))+6
		if path[(termwidth-((2*len(str(tot)))+6)):]:
			path=f'...{path[-(termwidth-((2*len(str(tot)))+6))]:}'
		return path.ljust(termwidth-part1)
		
	ppath=format_path(path)
	org_progress()
	stdwrite_string('[')
	stdwrite_string(cur)
	stdwrite_string('/')
	stdwrite_string(str(tot))
	stdwrite_string(']')
	loc()
	stdwrite_string(ppath)
	time.sleep(0.02)
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




cpy('/home/hoefkens/.bash/','.')




