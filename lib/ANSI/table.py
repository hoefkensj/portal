#!/usr/bin/env python

import shutil
import sys
import time
import time


def fn(fn):
	def ansi(SEQ):
		def ANSIseq(ESC='\033', SEQ='{SEQ}', FN='{FN}'):
			return '{ESC}[{SEQ}{FN}'.format(ESC=ESC,SEQ=SEQ,FN=FN)
		return ANSIseq(SEQ=SEQ,FN=fn)
	return ansi
'''
A 	Cursor Up 	(n=1) 	Move cursor up by n
B 	Cursor Down 	(n=1) 	Move cursor down by n
C 	Cursor Forward 	(n=1) 	Move cursor forward by n
D 	Cursor Back 	(n=1) 	Move cursor back by n

E 	Cursor Next Line 	(n=1) 	Move cursor to the beginning of the line n lines down
F 	Cursor Previous Line 	(n=1) 	Move cursor to the beginning of the line n lines up
G 	Cursor Horizontal Absolute 	(n=1) 	Move cursor to the the column n within the current row
H 	Cursor Position 	(n=1, m=1) 	Move cursor to row n, column m, counting from the top left corner

J 	Erase in Display 	(n=0) 	Clear part of the screen. 0, 1, 2, and 3 have various specific functions
K 	Erase in Line 	(n=0) 	Clear part of the line. 0, 1, and 2 have various specific functions

S 	Scroll Up 	(n=1) 	Scroll window up by n lines
T 	Scroll Down 	(n=1) 	Scroll window down by n lines

s 	Save Cursor Position 	() 	Save current cursor position for use with u
u 	Restore Cursor Position 	() 	Set cursor back to position last saved by s
f 	… 	… 	(same as G)
'''

E= fn('E')
F= fn('F')
G= fn('G')
H= fn('H')
K= fn('K')
L= fn('L')
M= fn('M')

table1={
		'T' : [['title'],['subtitle']], 								# T TITLES
		'H'	:	['\033[1m\033[4midx','header1','header2\033[0m'],							# H HEADERS
		'M'	:	{
						'tb':{False},
						'cb':{True},
						'fs'	: '\u250B',
						'pd'	: '\t',
						'mg'	: ' ',
						'al':'left'
					},							# M META
		'D'	:	[
					[1,'d2','123'],
					[5,'data\tp2','\033[1msomedata ',],
					[3,'\033[32mGreen\033[0m','data5299'],
					],
		'F'	:	[['help'],['footer']]
	}
table2={
		'T' : [['{title}'],['{subtitle}']], 								# T TITLES
		'H'	:	['{h-idx}','h-1','h-n','h-sub'],							# H HEADERS
		'M'	:	{ # Meta
						'B':{ #Border
							'Tbl':{0,0,0,0},
							'Col':{0,1,0,0}, #LCRB # |Lc|c_b_c|c|cR|
							'style': {1,1},
							'v_sbl': '\u250B',
							'h_sbl':	'',
							'Xoff': 0,
							'Yoff': 0,
							},
						'LC_pd'	: '\t',
						'RC_pd'	:	'\t',
						'mrgn'	:	' ',

						'al':'left'
					},							# M META
		'D'	:	[ # Data
					[1,'{D:0,1}}','da1ta2'],
					[2,'      ','\033[1msomedata ',],
					[f'\033[32m{3}','selected row','data5299\033[0m'],
					],
		'F'	:	[['help'],['footer']]
	}





def tty_writesbl(s):
	def stdout_write():
		sys.stdout.write(s)
		sys.stdout.flush()
		return tty_len()
	return stdout_write

	


def std_wr(s):
	sys.stdout.write(str(s))
	sys.stdout.flush()


def terminal_width(**k):
	stored=k.get('stored')
	width=(shutil.get_terminal_size()[0]-2)
	stored+=[width]
	diff=(-1*(stored[-2]-stored[-1]))
	return stored

def std_cursorloc():
	import termios
	import tty
	import re
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

def presets_re():
	import types
	import re
	preset = types.SimpleNamespace()
	preset.repl_ANSIm = re.compile(r'\033\[[;\d]*m',re.VERBOSE).sub
	preset.repl_ESCt = re.compile(r'\t',re.VERBOSE).sub
	return preset

def tty_len(**k):
	re=presets_re()
	wtab= '\u0020' * (k.get('t') or 4)
	s=str(k.get('s'))
	s=re.repl_ESCt(wtab,str(s))
	s=re.repl_ANSIm('',str(s))
	return len(s)

def pivot_mtx(mtx) -> list:
		return [[mtx[c[0]][r[0]] for c in enumerate(r[1])] for r in enumerate(mtx)]

def dcon_table(**k):
	import types
	table=k.get('tbl')
	tbl=types.SimpleNamespace()
	tbl.titles				=	table.get('T')
	tbl.headers				=	table.get('H')
	tbl.footers				=	table.get('F')
	tbl.data					=	table.get('D')
	tbl.meta					=	types.SimpleNamespace()
	tbl.meta.fs				=	table.get('M').get('fs')
	tbl.meta.pd				=	table.get('M').get('pd')
	tbl.meta.al				=	table.get('M').get('al')
	return tbl

def calc_dimensions(**k):
	tbl=dcon_table(**k)
	def lst_pdd(**k) -> list:
		tbl=dcon_table(**k)
		if tbl.meta.al=='left' or tbl.meta.al == 'right':
			lst_pd=[tty_len(s=tbl.meta.pd) for  ncol in range(len(tbl.headers))]
		else : #default = center
			lst_pd=[tty_len(s=tbl.meta.pd)*2 for  ncol in range(len(tbl.headers))]
		return lst_pd
	def lst_datamax(**k) -> list:
		tbl=dcon_table(**k)
		mtx=mtx_dataw(**k)
		piv=pivot_mtx(mtx)
		return [max(col) for idx,col in enumerate(piv)]
	def lst_cellw(**k) -> list:
		return [(data+padd) for data,padd in zip(lst_datamax(**k), lst_pdd(**k))]
	def lst_ltorg(**k) -> list:
		lst_leftbounds=[0,]
		lst_cellbwidths=[0,]+[i + tty_len(s=tbl.meta.fs) for i in lst_cellw(**k)]
		lst_leftbounds+=[lst_cellbwidths[i] + cell + tty_len(s=tbl.meta.fs) for i,cell in enumerate(lst_cellw(**k)[:-1])]
		return lst_leftbounds
	def lst_fsorg(**k) -> list:
		tbl=dcon_table(**k)
		return [x - tty_len(s=tbl.meta.fs) for x in lst_ltorg(**k)[1:]]
	
	def lst_stdw_ltorg(**k) -> list:
		return [tty_writesbl(s=G(lb)) for lb in lst_ltorg(**k)]
	def lst_stdw_fsorg(**k) -> list:
		return [tty_writesbl(s=G(pd)) for pd in lst_fsorg(**k)]
	
	def mtx_dataw(**k) -> list:
			return [[tty_len(s=cell) for cell in row] for row in tbl.data]
	def mtx_relorg(**k) -> list:
		return 	[[[f'{F(r)}{G(lst_cellw(**k)[c])}'] for c, cell in enumerate(tbl.data[r])] for  r,row in enumerate(tbl.data)]
	
	def mtx_tblsurfaace():
			# cell= padd[:x]+data+padd[x:]
			# fs= mg+fs+mg
			cells_dmy=[str().ljust(mx+tty_len(tbl.meta.pd),'#') for mx in lst_datamax()]
			fs_dummy=[str().ljust(2*tty_len(tbl.meta.mg) + tty_len(tbl.meta.fs) )]
			row_dmy=''cells_dmy
			
	
	def tbl_dim(fn,tbl):
		def calc():
			return fn(tbl=tbl)
		return calc()
	
	def calc():
		import types
		calc									= types.SimpleNamespace()
		calc.lst_pdd					= tbl_dim(lst_pdd, k.get('tbl'))						#				[4, 4, 4]
		calc.lst_collw				=	tbl_dim(lst_datamax, k.get('tbl'))					#		+___[5, 10, 9]
		calc.lst_cellw				= tbl_dim(lst_cellw, k.get('tbl'))					#		=		[9, 14, 13] __/_+2
		calc.lst_ltorg				=	tbl_dim(lst_ltorg, k.get('tbl'))					#		[0, 11, 27] 		/	+ =
		calc.lst_fsorg				=	tbl_dim(lst_fsorg, k.get('tbl'))					#			[9, 25] 			| field separator
	
		calc.lst_stdw_ltorg		=	tbl_dim(lst_stdw_ltorg, k.get('tbl'))
		calc.lst_stdw_fsorg		=	tbl_dim(lst_stdw_fsorg, k.get('tbl'))
		calc.mtx_dataw				= tbl_dim(mtx_dataw,k.get('tbl'))						#				[	[1, 2, 3], [[['\x1b[0F\x1b[9G'], ['\x1b[0F\x1b[14G'], ['\x1b[0F\x1b[13G']],
		calc.mtx_relorg				=	tbl_dim(mtx_relorg,k.get('tbl'))					#					[5, 10, 9]	[['\x1b[1F\x1b[9G'], ['\x1b[1F\x1b[14G'], ['\x1b[1F\x1b[13G']]
		return calc																												#					[1, 5, 8]]	[['\x1b[2F\x1b[9G'], ['\x1b[2F\x1b[14G'], ['\x1b[2F\x1b[13G']]]
	
	return calc()
	

def listprt(lst):
	for tem in lst:
		print(repr(tem),'\n\n')
def listprt2(lst):
	print('fn')
	for tm in lst:
		[print((t())) for t in tm]
calc=calc_dimensions(tbl=table1)
listprt([calc.lst_pdd,calc.lst_collw,calc.lst_cellw,calc.lst_ltorg,calc.lst_fsorg,calc.mtx_dataw,	calc.mtx_relorg,])
listprt2([calc.lst_stdw_ltorg])
listprt2([calc.lst_stdw_fsorg])


calc= calc_dimensions(tbl=table1)
mtx_relorg = calc.mtx_relorg
stdw_table=[]
tbl=dcon_table(tbl=table1)
for r,row in enumerate(tbl.data):
	for	c,cell in enumerate(row):
		calc.lst_stdw_ltorg[c]()
		(calc.lst_stdw_ltorg[c](),std_wr(tbl.data[r][c]))
		[(b(),std_wr(f'\033[0m{tbl.meta.fs}')) for b in calc.lst_stdw_fsorg]
	std_wr('\n')

row_next=tty_writesbl(s=M('10;10'))



# tpl_org=std_cursorloc()
# tbl_org=ANSI_H(f'{tpl_org[1]};{tpl_org[0]}')
# tpl_org=std_cursorloc()
dat_org=H('2;0')#ANSI_H(f'{tpl_org[1]+2};{tpl_org[0]}')

# def fn(fnx):
# 	time.sleep(1)
# 	sys.stdout.write(f'{fnx}1');sys.stdout.flush()
# 	time.sleep(1)
# 	sys.stdout.write(f'\033[10{fnx}');sys.stdout.flush()
# 	time.sleep(1)
# 	sys.stdout.write(f'{fnx}2');sys.stdout.flush()
# 	time.sleep(1)
#
# import string
# alfab=string.ascii_uppercase
# print(alfab)
# for f in alfab:
# 	fn(f)
	



# 	def tmp():
# 		for r,row in enumerate(tbl_data):
# 			for c,cell in enumerate(row):
# 				sys.stdout.write(f'\033[{calc_leftbounds()[c]}G{cell}')
# 			for b,border in enumerate(calc_borderorg()):
# 				sys.stdout.write(f'\033[0m\033[{calc_borderorg()[b]}G{fs}')
# 			sys.stdout.write('\n')
#
#
#
# # [print(row) for row in rows]
# # print()
# # print()
#
# upper = [chr(i) for i in range(65, 91)]
# lower = [chr(i) for i in range(96, 123)]
#
#
#
# calc_dimensions(tbl=table1)
#
# calc_dimensions(tbl=table2)


mv 620be3deaf705.mp4 wget/
mv 6207ea6b0e5df.mp4 wget/
mv 620b29c2a008c.mp4 wget/
mv 620b21e8516e6.mp4 wget/
mv 6207e27fa9a41.mp4 wget/
mv 5f129df044db6.mp4 wget/
