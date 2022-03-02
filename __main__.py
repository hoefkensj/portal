#!/usr/bin/env python
import cli

def user():
	import main
	main.env_store()
	
def root():
	import main
	print(f'running as  UID: {os.geteuid()} ({os.environ.get("USER")}) [OK]')
	main.env_load()

if __name__ == '__main__':
	cli.cli()
