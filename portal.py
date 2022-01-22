#!/usr/bin/env python
import os,sys,shlex,shutil
import subprocess as sproc
import timeit
# timer = timeit.default_timer

#	lets not redefine build-ins anymore
#	sprint=sys.stdout.write
# NOR:
# def print(*a):
# 	print_str=''
# 	for char_str in a:
# 		print_str=f'{print_str}{str(char_str)}'
# 	sys.stdout.write(print_str)
	
def robocopy(srcdir,dest) -> None:
	flags='/E /COPYALL /SJ /SL /L'
	popen=sproc.Popen(shlex.split(f'robocopy /E /COPY:DATSO /SJ /SL /L {srcdir} {dest}'),stdout=sproc.PIPE,universal_newlines=True)
	for line in iter(popen.stdout.readline,''):
		yield '/'.join(line.split('->')[0].split('/')[len(srcdir.split('/')):])
	popen.stdout.close()
	return_code=popen.wait()
	if return_code:
		raise sproc.CalledProcessError(return_code,cp)

def cp(srcdir, dest) -> None:
	"""
	Copies files form srcdir to dest, returns stdout in pipe in realtime
	"""
	proc_cp = sproc.Popen(shlex.split(f'cp -rvp{"f" if force else ""} {srcdir} {dest}'), stdout=sproc.PIPE, universal_newlines=True)
	for line in iter(proc_cp.stdout.readline, ''):
		yield '/'.join(line.split('->')[0].split('/')[len(srcdir.split('/')):])
	proc_cp.stdout.close()
	return_code = proc_cp.wait()
	if return_code:
		raise sproc.CalledProcessError(return_code, cp)

def count(pdf,tot=[]):
	tot += [(len(pdf[1]) + len(pdf[2]))]
	sys.stdout.write(f'\033[4G\u001b[38;5;123m{sum(tot)}]\u001b[0m')
	return sum(tot)

def format_copy_line(line):
	termwidth=shutil.get_terminal_size()[0]
	if line[(termwidth-4):]:
		line = f'{line[:termwidth-4]}...'
	return line
	
def updatebar(line,tot,cur):
	line=f"[\033[2G\u001b[38;5;123m{cur}\u001b[0m/{tot}] {line}"
	sys.stdout.write(format_copy_line(line))
	return cur

def cpy(srcdir, dest,force=False) -> None:
	"""
	copy progress
	"""
	copy = robocopy if os.name == 'NT' else cp
	sys.stdout.write('Checking:\033[1E[0/0]')
	total = [count(pdf) for pdf in os.walk(srcdir,topdown=True)]
	sys.stdout.write(f'\033[1F\033[11Done\tCopying:')
	start_timer=timeit.default_timer()
	cur=[updatebar(line,sum(total),idx) for idx,line in enumerate(copy(srcdir, dest))]
	end_timer=timeit.default_timer()
	sys.stdout.write(f'Copying: Done (Copied {cur[-1]} files of {sum(total)} in {end_timer - start_timer}s)')
	
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
		# gets the number of common folders in the paths of src and lnk  2 = /test/ikkel/src,/test/ikkel/to/lnk
		common =len([sf for sf, lf in zip(src.split('/'),lnk.split('/')) if sf == lf ])
		# {'./' if src and lnk are in the same folder else ''}
		sibling='./' if len(lnk.split('/')[common:-1])<1 else ''
		# {.. for ever folder in lnk that is not in dst creating ['..','..' ...]
		src=f"{sibling}{'/'.join(['..' for folder in lnk.split('/')[common:-1]]+src.split('/')[common:-1]+[os.path.split(src)[1]])}"
	os.symlink(src,lnk)

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
		'link'	: link,
		}
	method=methods[method]
	copy(src,dst)
	rmr(src)
	method(dst,src,rel)













