#!/usr/bin/env python
import types
import collections
import string



def main():
	pass


if __name__ == '__main__':
	main()


def fn(fn):
	def ansi(SEQ):
		def ANSIseq(ESC='\033', SEQ='{SEQ}', FN='{FN}'):
			return '{ESC}[{SEQ}{FN}'.format(ESC=ESC,SEQ=SEQ,FN=FN)
		return ANSIseq(SEQ=SEQ,FN=fn)
	return ansi
def markup(*a,**k):
	from . import markup
	return
	

# def ANSI(**k) -> types.SimpleNamespace:
# 	"""
# 	returns the namespace for all ansi functions
# 	:param k: keywords : [ns,]
# 	:keyword ns: a namespace to work with this can just be "types.SimpleNamespace"
# 	:return: the ansi functions in a Namespace where namespace.$[a-Z] ~\033[x;x;x$[a-Z]
# 	"""
# 	NS		=	k.get('ns')
# 	NS.A	=	fn('E')
# 	NS.B	=
# 	NS.C	=
# 	NS.D	=
# 	NS.E	= fn('E')
# 	NS.F	= fn('F')
# 	NS.G	= fn('G')
# 	NS.H	= fn('H')
# 	NS.I
# 	NS.J
# 	NS.K	= fn('K')
# 	NS.m	= fn('m')
# 	return ANSI
#
#
# ANSI=ANSI()
# ANSI_E= fn('E')
# ANSI_F= fn('F')
# ANSI_G= fn('G')
# ANSI_H= fn('H')
# ANSI_K= fn('K')
# ANSI_m= fn('m')


# ANSI.m=fn('m')
print(string.ascii_letters)
