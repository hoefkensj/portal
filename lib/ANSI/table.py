#!/usr/bin/env python

import shutil
import time
import sys

def fn(fn):
	def ansi(SEQ):
		def ANSIseq(ESC='\033', SEQ='{SEQ}', FN='{FN}'):
			return '{ESC}[{SEQ}{FN}'.format(ESC=ESC,SEQ=SEQ,FN=FN)
		return ANSIseq(SEQ=SEQ,FN=fn)
	return ansi



ANSI_E= fn('E')
ANSI_F= fn('F')
ANSI_G= fn('G')
ANSI_H= fn('H')
ANSI_K= fn('K')

table1={
		'T' : [['title'],['subtitle']], 								# T TITLES
		'H'	:	['\033[1m\033[4midx','header1','header2\033[0m'],							# H HEADERS
		'M'	:	{
						'tb':{False},
						'cb':{True},
						'fs'	: '\u250B ',
						'pd'	: '\t',
						'al':'left'
					},							# M META
		'D'	:	[
					[1,'da1312312312545a1','da1ta2'],
					[55582,'data\t1','\033[1msomedata ',],
					[3,'\033[32mGreen\033[0m','data5299'],
					],
		'F'	:	[['help'],['footer']]
	}
table2={
		'T' : [['title'],['subtitle']], 								# T TITLES
		'H'	:	['\033[1m\033[4midx','header1','header2\033[0m'],							# H HEADERS
		'M'	:	{
						'tb':{False},
						'cb':{True},
						'fs'	: '\u250B ',
						'pd'	: '\t',
						'al':'left'
					},							# M META
		'D'	:	[
					[1,'\t\t\t','da1ta2'],
					[2,'      ','\033[1msomedata ',],
					[f'\033[32m{3}','selected row','data5299\033[0m'],
					],
		'F'	:	[['help'],['footer']]
	}


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

def calc_dimensions(**k):
	"""
	legenda:
	fs= fieldseparator pd=padding
	|	title				| subtitle			|
	|	idx	|	head1	| head2	|	head3	|
	|		1	|	data1	|	data2	|				|
	
	example:
	:param k:
	:return:
	"""
	table=k.get('tbl')
	tbl_titles=k.get('tbl')['T']
	tbl_headers=k.get('tbl')['H']
	tbl_footers=k.get('tbl')['F']
	tbl_data=k.get('tbl')['D']
	fs=k.get('tbl')['M'].get('fs')
	pd=k.get('tbl')['M'].get('pd')
	al=k.get('tbl')['M'].get('al')
	
	ncolls	=	len(tbl_headers)
	nrows		=	len(tbl_data)
	
	def calc_padding() -> list:
		if al=='left' or al == 'right':
			lst_pd=[tty_len(s=pd) for  ncol in range(ncolls)]
		else : #default = center
			lst_pd=[tty_len(s=pd)*2 for  ncol in range(ncolls)]
		return lst_pd

	def calc_datawidths() -> list:
		matrix_datawidths=[]
		for row in table['D']:
			lst_datawidths = []
			for cell in row:
				lst_datawidths+= [tty_len(s=cell)]
			matrix_datawidths=[*matrix_datawidths,lst_datawidths]
		return matrix_datawidths
	
	def pivot_matrix(m) -> list:
		return [[m[c[0]][r[0]] for c in enumerate(r[1])] for r in enumerate(m)]
		
	def calc_colldatawidths() -> list:
		lst_colldatawidths=[0 for h in table['H']]
		matrix_datawidths=calc_datawidths()
		matrix_pivotdw=pivot_matrix(matrix_datawidths)
		for idx,col in enumerate(matrix_pivotdw):
			lst_colldatawidths[idx]=max(matrix_pivotdw[idx])
		return lst_colldatawidths
	
	def calc_cellwidths():
		lst_colldatawidths=calc_colldatawidths()
		lst_padd=calc_padding()
		colwidths=[(data+padd) for data,padd in zip(lst_colldatawidths,lst_padd)]
		return colwidths
		
	def calc_leftbounds(**k):
		lst_leftbounds=[0,]
		lst_cellbwidths=[0,]+[i+tty_len(s=fs) for i in calc_cellwidths()]
		lst_leftbounds+=[lst_cellbwidths[i]+cell+tty_len(s=fs) for i,cell in enumerate(calc_cellwidths()[:-1])]
		return lst_leftbounds
	
	def calc_borderorg():
		borderb=[x-tty_len(s=fs) for x in calc_leftbounds()[1:]]
		return borderb
		

	tpl_org=std_cursorloc()
	tbl_org=ANSI_H(f'{tpl_org[1]};{tpl_org[0]}')
	tpl_org=std_cursorloc()
	dat_org=ANSI_H(f'{tpl_org[1]+2};{tpl_org[0]}')
	lst_lbounds=calc_leftbounds()
	lst_cellwidths=calc_cellwidths()
	lst_borderorg=calc_borderorg()
	
	def calc_locs():
		H = [ANSI_G(lst_lbounds[i])for i,header in enumerate(tbl_headers)]
		matrix_dataloc=[]
		for r,row in enumerate(tbl_data):
			loc_row=[]
			for c,cell in enumerate(tbl_data[r]):
				loc_row+=[f'{dat_org}{ANSI_F(r)}{ANSI_G(calc_leftbounds()[c])}']
		matrix_dataloc+=loc_row
		return matrix_dataloc
	
	print('locs:',calc_locs())
	matrix_locs=calc_locs()
	for r,row in enumerate(tbl_data):
		for c,cell in enumerate(row):
			sys.stdout.write(f'{matrix_locs[r][c]}{tbl_data[r][c]}')
		
		
		
	def tmp():
		for r,row in enumerate(tbl_data):
			for c,cell in enumerate(row):
				sys.stdout.write(f'\033[{calc_leftbounds()[c]}G{cell}')
			for b,border in enumerate(calc_borderorg()):
				sys.stdout.write(f'\033[0m\033[{calc_borderorg()[b]}G{fs}')
			sys.stdout.write('\n')



# [print(row) for row in rows]
# print()
# print()

upper = [chr(i) for i in range(65, 91)]
lower = [chr(i) for i in range(96, 123)]


print('table1:')

calc_dimensions(tbl=table1)
print('\ntable2:')
calc_dimensions(tbl=table2)