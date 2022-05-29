#!/usr/bin/env python
import click as C

from . import cpy


@C.group()
@C.pass_context
def entry_point(ctx):
	"""Portal Help """
	# ensure that ctx.obj exists and is a dict (in case `cli()` is called
  # by means other than the `if` block below)
	ctx.ensure_object(dict)


entry_point.add_command(cpy.copy)




