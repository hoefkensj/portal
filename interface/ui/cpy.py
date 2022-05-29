#!/usr/bin/env python3
#[DOCS]
'''	'''
#[CODE]
import sys

import click as C
import portal.fnx.cpy


@C.command()
@C.argument('src',required=True,type=str)
@C.argument('dst',required=True,type=str)
@C.pass_context
def copy(ctx,src, dst) -> None:
	"""
	\b
	SRC = Source to copy
	DST = Destination to where to copy
	\b
	COPY uses the copy method to create a protal:
		1: /path/[src] -> copy -> /path/[dst]/[src]
		2: /path/[src] -> rm -r -> /path/
		3:	see: link or bind
		
	note: This will be slower when [src] and [dst] ar on the same filesystem
	\f
	:param src: source
	:param dst: destination
	
	"""
	portal.fnx.cpy.cpy_cli()
	
	
sys.stdout.write('\u001b[1E')
sys.stdout.write('Portal: \u001b[32mCopy\u001b[0m')
sys.stdout.write('\033[38;5;123m'+'Checking'+'\033[0m:')
sys.stdout.write('\033[1E')
sys.stdout.write('[0/0]')
sys.stdout.write('\033[1E')

	


