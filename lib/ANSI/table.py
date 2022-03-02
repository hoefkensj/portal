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




def tabledata_width(**k):
	flags=k.get('flags')
	#sym shrink idx mark
	pass
	
def terminal_width(**k):
	stored=k.get('stored')
	width=(shutil.get_terminal_size()[0]-2)
	stored+=[width]
	diff=(-1*(stored[-2]-stored[-1]))
	print(stored[-2],stored[-1],diff)
	return stored
stored=[0,]
stored = terminal_width(stored=stored)
stored = terminal_width(stored=stored)
stored = terminal_width(stored=stored)

table={
		'T' : [['title'],['subtitle']], 								# T TITLES
		'H'	:	['idx','header1','header2'],							# H HEADERS
		'M'	:	{'fs'	: '|','pd'	: '    '},							# M META
		'D'	:	[
					[1,'da1312312312545a1','da1ta2'],
					[55582,'data1','r212'],
					[3,'r','data5299'],
					],
		'F'	:	[['help'],['footer']]
	}
cols={}


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
	tbl_titles=k.get('tbl')['T']
	tbl_headers=k.get('tbl')['H']
	tbl_footers=k.get('tbl')['F']
	tbl_data=k.get('tbl')['D']
	fs=k.get('tbl')['M'].get('fs')
	pd=k.get('tbl')['M'].get('pd')


	def calc_datawidths():
		
		# lst_datawidths=[0 for item in tbl_headers]
		# matrix_datawidths=[lst_datawidths for  row in table['D']]
		
		matrix_datawidths=[]
		for row in table['D']:
			lst_datawidths = []
			for cell in row:
				lst_datawidths+= [len(str(cell))]
			matrix_datawidths=[*matrix_datawidths,lst_datawidths]
		return matrix_datawidths
	
	matrix_datawidths = calc_datawidths()
	print(repr(matrix_datawidths))




	def calc_leftbounds(**k):
		def strw(a,i):
			return len(str(table['D'][a][i]))

		lst_colwidths=[0 for item in tbl_headers]
		for a,_ in enumerate(table['D'][0]):
			for i,_ in enumerate(table['D']):
				lst_colwidths[i]=max(strw(a,i) ,lst_colwidths[i])
		lst_colwidths=[colw+len(fs)+len(pad*2) for colw in lst_colwidths]
		
		tbl_w=sum(lst_colwidths)
		titw=divmod(tbl_w,len(tbl_titles))[0]
		x_tits=[0 for i in tbl_titles]
		x_tits= [1+(n*titw) for n,i in enumerate(x_tits)]
		tmp_hds=[0, *lst_colwidths]
		x_hds=[0 for item in lst_colwidths]
		for  n,i in enumerate(lst_colwidths):
			if n == 0 :
				x_hds[n]=1
			else:
				x_hds[n]=x_hds[n-1]+tmp_hds[n]
		return x_hds

# print(repr(calc_leftbounds(tbl=table)))
# col_lbds= calc_leftbounds(tbl=table)
fs=table.get('M').get('fs')
pd=table.get('M').get('pad')
# for nr,row in enumerate(table['D']):
# 	for x,col in zip(col_lbds,row):
# 		sys.stdout.write(f'{ANSI_G(x)}{fs}{pd}{col}{pd}')
# 	sys.stdout.write(f'{pd}{fs}\n')


def lister(data,rows=[]):
	
	if isinstance(data,list):
		itemset=[]
		for item in data:
			if isinstance(item,list):
				lister(item)
			else:
				itemset+=[str(item)]
		rows+=[itemset]
	return rows
rows=lister(table)

# [print(row) for row in rows]
# print()
# print()

upper = [chr(i) for i in range(65, 91)]
lower = [chr(i) for i in range(96, 123)]
# [sys.stdout.write(chr(i)) for i in range(65, 91)]
enumerate(table)
# def alfa(val):

#
calc_dimensions(tbl=table)