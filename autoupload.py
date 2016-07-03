#!/usr/local/bin/python3
import subprocess
import sys

try:
	comment = sys.argv[1]
except IndexError:
	comment = "Minor fix"

subprocess.call(['git', 'add', '.'])
subprocess.call(['git', 'rm', '-rf', '__pycache__'])
subprocess.call(['git', 'commit', '-m', comment])
subprocess.call(['git', 'push', 'heroku', 'master'])