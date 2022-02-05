#!/usr/bin/env python
import re
import sys
import termios
import tty
import types
import shutil

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

def stdwrite_org_H(ANSI_cursor):
	ansi='\033[{n};{m}H'.format(n=ANSI_cursor[0],m=ANSI_cursor[1])
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
	termwidth = shutil.get_terminal_size()[0]
	col_1 = (1, ((termwidth / 2) - 1))
	col_2 = (((termwidth / 2) + 1), (termwidth - 1))
	def defaults():
			k['DEFAULT'] = {'t1': col_1[0], 't2': col_2[0], 'ts': 12}
			k['t1'] = k.get('t1') or k['DEFAULT'].get('t1')
			k['t2'] = k.get('t2') or k['DEFAULT'].get('t2')
			k['ts'] = k.get('ts') or k['DEFAULT'].get('ts')
	defaults()
	org = types.SimpleNamespace()
	curs_init_row= std_cursorloc()[0]
	curs_init_col= std_cursorloc()[1]
	org.init						=	stdwrite_org_H([(curs_init_row-2),curs_init_col])	# ROWS:
	org.header					=	stdwrite_org_H([(curs_init_row-2),1])
	org.progress				=	stdwrite_org_H([(curs_init_row-1),1])
	# COLS
	org.title_1					=	stdwrite_org_G((k.get('t1')))
	org.title_1_stat		=	stdwrite_org_G((k.get('t1')+k.get('ts')))
	org.title_2					=	stdwrite_org_G((k.get('t2')))
	org.title_2_stat		=	stdwrite_org_G((k.get('t2')+k.get('ts')))
	org.proc						=	stdwrite_org_G((k.get('ts')))
	org.count						=	stdwrite_org_G((k.get('ts')+2))
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
	
	return clr