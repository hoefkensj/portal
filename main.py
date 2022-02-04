#!/usr/bin/env python
import os
import lib
import fnx.portal_link


def force(method,src,dst):
	method(src,dst,force=True)
	return method

def bind():
	pass

def end(reason):
	print(reason)
	exit()

def portal(src, dst, method, force, rel) -> None:
	ar_dst=os.path.abspath(os.path.realpath(dst)) #a(bsolute)r(eal)_dst
	if os.path.islink(src):
		end(reason=f'ERROR: source ({src}) is a link')
	if os.path.abspath(dst) == os.path.abspath(src):
		end(reason=f'ERROR source({src}) and destination({dst}) are the same')
	copy=(force(cpy, src, dst) if force else end(reason=f'ERROR {os.path.abspath(dst)} exists (use --force to overwrite)')) if os.path.exists(dst)	else cpy
	methods={
		'bind' : bind,
		'link'	: fnx.portal_link.link,
		}
	method=methods[method]
	copy(src,dst)
	rmr(src)
	method(dst,src,rel)



if __name__ == '__main__':
	cpy('/home/hoefkens/Development/TestingGrounds/testsrcdir', '/home/hoefkens/Development/TestingGrounds/testdstdir/')





