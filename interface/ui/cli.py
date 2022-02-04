#!/usr/bin/env python
import click as C


@C.group()
def entry_point():
	"""Portal Help """
	pass


from . import cpy
entry_point.add_command(cpy.copy)

entry_point()



