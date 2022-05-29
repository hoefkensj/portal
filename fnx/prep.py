#!/usr/bin/env python
import os
import os
import shutil

import lib
import lib.lib


src='$HOME/.bashrc'
def prep_src(src,**k):
	"""
	
	:param src:
	:param k:
	:return:
	"""
	#this needs to be don before actually creating the propsdict as they arent done automaticly
	if "~" in src or '$' in src:
		src=os.path.expandvars(src)
		src=os.path.expanduser(src)
	props= props_path(src)
	#avoid this , complex behavior
	if props['islink'] and ('--copy-contents' in [k.get('flags')] or '--follow-links' in  [k.get('flags')] ):
		print('flag detected')
		src=props['realpath']
		props=props= props_path(src)
		
	for key in props.keys():

		print(key,'\t:\t',props[key])

prep_src(src,flags='--copy-contents')

#!/usr/bin/env python

def prep_dst(dst,src_meat,**k):
	"""
	
	:param src:
	:param k:
	:return:
	"""
	#this needs to be don before actually creating the propsdict as they arent done automaticly
	if "~" in dst or '$' in dst:
		dst=os.path.expandvars(dst)
		dst=os.path.expanduser(dst)
	props_dst= props_path(dst)
	props_dstsrc= props_path(os.path.join(dst, src_meat))
	
	if not props_dst['exists']:
		os.makedirs(dst)
	if props_dstsrc['exists']:
		#cannot copy use merge instead
		method='merge'
		
	
	if props_dst['islink']:
		dst=props_dst['realpath']
		props_dst= props_path(dst)
	
	dst=props_dst['abspath']

def rmr(path) -> None:
	shutil.rmtree(path)

def props_path(src) -> dict:
	props={}
	for fn in [(item,fn) for item,fn in os.path.__dict__.items() if callable(fn)]:
		try: props[fn[0]]=fn[1](src)
		except Exception as ERROR: props[fn[0]]=f'#!_ERROR :{ERROR}'
	return props