#!/usr/bin/env python
import types

def fn(fn):
	def ansi(SEQ):
		def ANSIseq(ESC='\033', SEQ='{SEQ}', FN='{FN}'):
			return '{ESC}[{SEQ}{FN}'.format(ESC=ESC,SEQ=SEQ,FN=FN)
		return ANSIseq(SEQ=SEQ,FN=fn)
	return ansi

def fn_m():
	return fn('m')

def m():
	markup= fn_m()
	
	def rgb(t):
		def fn(rgb,*a):
			if a:
				return markup('{t};2;{r};{g};{b}'.format(t=t,r=rgb,g=a[0],b=a[1]))
			else:
				return markup('{t};2;{r};{g};{b}'.format(t=t,r=rgb[1:2],g=rgb[3:4],b=rgb[5:6]))
		return fn

	m						=	types.SimpleNamespace()	#	0 - 9
	m.reset			=	markup(0)
	m.bold			=	markup(1)
	m.faint			=	markup(2)
	m.italic		= markup(3)
	m.uline			=	markup(4)
	m.sblink		=	markup(5)
	m.fblink		= markup(6)
	m.inv				=	markup(7)
	m.hide			= markup(8)
	m.strike		=	markup(9)
	m.font			=	types.SimpleNamespace()	#	10 - 19	#	A - J
	m.font.A		=	markup(10)
	m.font.B		= markup(11)
	m.font.C		= markup(12)
	m.font.D		= markup(13)
	m.font.E		= markup(14)
	m.font.F		= markup(15)
	m.font.G		= markup(16)
	m.font.H		= markup(17)
	m.font.I		= markup(18)
	m.font.J		= markup(19)
	m.duline		=	markup(21)

	m.no 				= types.SimpleNamespace()
	m.no.uline	= markup(24)
	m.no.blink	=	markup(25)
	m.no.strike	=	markup(29)
	
	m.fg					=	types.SimpleNamespace()
	m.fg.black		=	markup(30)
	m.fg.red			=	markup(31)
	m.fg.green		=	markup(32)
	m.fg.yellow		=	markup(33)
	m.fg.blue			=	markup(34)
	m.fg.magenta	=	markup(35)
	m.fg.cyan			=	markup(36)
	m.fg.white		=	markup(37)
	m.fg.rgb			= rgb(38)
	m.bg					=	types.SimpleNamespace()
	m.bg.black		=	markup(40)
	m.bg.red			=	markup(41)
	m.bg.green		=	markup(42)
	m.bg.yellow		=	markup(43)
	m.bg.blue			=	markup(44)
	m.bg.magenta	=	markup(45)
	m.bg.cyan			=	markup(46)
	m.bg.white		=	markup(47)
	m.bg.rgb			= rgb(48)
	m.black				=	markup(30)
	m.red					=	markup(31)
	m.green				=	markup(32)
	m.yellow			=	markup(33)
	m.blue				=	markup(34)
	m.magenta			=	markup(35)
	m.cyan				=	markup(36)
	m.white				=	markup(37)
	m.rgb					= rgb(38)
	m.bblack			=	markup(40)
	m.bred				=	markup(41)
	m.bgreen			=	markup(42)
	m.byellow			=	markup(43)
	m.bblue				=	markup(44)
	m.bmagenta		=	markup(45)
	m.bcyan				=	markup(46)
	m.bwhite			=	markup(47)
	m.brgb				= rgb(48)
	m.dct					= m.__dict__
	return m

def markup(*a):
	m()
	return ''.join([m.__dict__.get(arg) for arg in a])

def txt(**k) -> str:
	"""
	examples:
	print(str(txt(txt='test',markup=[0,'green','line',0])))
	print(str(txt(txt='ikkel',markup=['blue'])))
	print(str(txt(txt='ikkel',markup=['strike',0])))
	:param k:
	:return:
	"""
	m()
	str_styles='{placeholder}'
	style_chain=k.get('markup')
	if style_chain[0]==0: #=start with reset
		style_chain=style_chain[1:]
		str_styles=str_styles.format(placeholder='{reset}{placeholder}'.format(reset=m.reset,placeholder='{placeholder}'))
	if style_chain[-1]==0: #=stop with reset
		style_chain=style_chain[0:-1]
		str_styles=str_styles.format(placeholder='{placeholder}{reset}'.format(reset=m.reset,placeholder='{placeholder}'))
	for  style in style_chain:
		str_styles=str_styles.format(placeholder='{style}{placeholder}'.format(style=markup(style),placeholder='{placeholder}'))
	reset=m.reset
	text=str(k.get('txt'))
	return str_styles.format(placeholder=text,reset=reset)
	
def settxt(*a, **k):
	text= k.get('txt') if k.get('txt') else str().join(a) if a else ''
	styles=[style for style in k.get('style') if k.get('style')]
	txt_styled=txt(text=text, m=styles)
	def stdout_text():
		return str(txt_styled)
	return stdout_text()

def setstyle(**k):
	text='{placeholder}'
	styles=[style for style in k.get('style') if k.get('style')]
	txt_styled=txt(txt=text, markup=styles)
	def stdout_text(text):
		return str(txt_styled.format(placeholder=text))
	return stdout_text

def markup_test(**k):
	for style in m.dct.keys():
		print(m.dct[style],f'{style}',m.reset)
