#!/usr/bin/env python
import click as C
from fnx import portal


@C.command()
@C.argument('src',required=True,type=str)
@C.argument('dst',required=True,type=str)
@C.option('-b', '--bind','f_method' ,required=True, is_flag=True, flag_value='bind')
@C.option('-l', '--link','f_method',required=True, is_flag=True, flag_value='link' )
@C.option('-r','--rel' ,is_flag=True)
@C.option('-f','--force','f_force' ,is_flag=True)
def cli(src,dst,f_method,f_force,rel) -> None:
	"""
	Copies SRC to DST and replaces SRC with a 'Portal' to DST
	:param src: source
	:param dst: destination
	:param f_method: link or bind
	:param f_force: replace existing files in DST
	:param rel: creates symlink relative to src
	:return: None
	"""
	portal.portal(src, dst, f_method, f_force, rel)