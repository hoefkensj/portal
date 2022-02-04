#!/usr/bin/env python
#[DOCS]
'''	'''
#[CODE]
import os



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
		# gets the number of common folders in the paths of src and lnk  2 = /test/ikkel/src,/test/ikkel/to/lnk
		common =len([sf for sf, lf in zip(src.split('/'),lnk.split('/')) if sf == lf ])
		# {'./' if src and lnk are in the same folder else ''}
		sibling='./' if len(lnk.split('/')[common:-1])<1 else ''
		# {.. for ever folder in lnk that is not in dst creating ['..','..' ...]
		src=f"{sibling}{'/'.join(['..' for folder in lnk.split('/')[common:-1]]+src.split('/')[common:-1]+[os.path.split(src)[1]])}"
	os.symlink(src,lnk)