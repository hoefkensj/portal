#!/usr/bin/env python
import os,sys,shlex,shutil
import subprocess as sproc
import timeit
timer = timeit.default_timer
sprint=sys.stdout.write
def sprint(*a,**k):
	pass

def cpy(srcdir, dest,force=False) -> None:
	"""
	copy progress
	"""
	ANSI={
			'SOL'			:		f'\033[0F'	,
			'SOPL'		:		f'\033[1F'	,
			'CLL'			:		f'\033[2K'	,
	}
	
	
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
		popen = sproc.Popen(shlex.split(f'cp -rvp{"f" if force else ""} {srcdir} {dest}'), stdout=sproc.PIPE, universal_newlines=True)
		for line in iter(popen.stdout.readline, ''):
			yield '/'.join(line.split('->')[0].split('/')[len(srcdir.split('/')):])
		popen.stdout.close()
		return_code = popen.wait()
		if return_code:
			raise sproc.CalledProcessError(return_code, cp)
			
	def count(pdf,tot=[]):
		sub_tot = len(pdf[1]) + len(pdf[2])
		tot += [(sub_tot)]
		for i in range(1, sub_tot):
			print(f'[0/{sum(tot) + i}]')
			sprint(f"{ANSI['SOL']}{ANSI['CLL']}")
		return sub_tot
		
	def updatebar(line,tot,cur):
		def format_line(line):
			termwidth=shutil.get_terminal_size()[0]
			if line[(termwidth-4):]:
				line=f'{line[0:(termwidth-4)]}...'
			return line
		line=f"[{cur}/{tot}] {line}"
		print(format_line(line))
		sprint(f"{ANSI['SOL']}{ANSI['CLL']}")
		return cur
	
	cp = robocopy if os.name=='NT' else cp
	
	print('Checking:')
	total = [count(pdf) for pdf in os.walk(srcdir,topdown=True)]
	sprint(f"{ANSI['SOPL']}{ANSI['CLL']}")
	print(f'Checking: Done (Total: {sum(total)})')
	print(f'Copying:')
	start_timer=timer()
	cur=[updatebar(line,sum(total),idx) for idx,line in enumerate(cp(srcdir, dest))]
	end_timer=timer()
	sprint(f"{ANSI['SOPL']}{ANSI['CLL']}")
	print(f'Copying: Done (Copied {cur[-1]} files of {sum(total)} in {end_timer-start_timer}s)')
	
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
		common =len([sf for sf, lf in zip(src.split('/'),lnk.split('/')) if sf == lf ])
		src=f"{'./' if len(lnk.split('/')[common:-1])<1 else ''}{'/'.join(['..' for folder in lnk.split('/')[common:-1]]+src.split('/')[common:-1]+[os.path.split(src)[1]])}"
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













