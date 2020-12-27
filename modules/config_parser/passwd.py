# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

shell_ignore = ['/sbin/halt', '/usr/sbin/nologin', '/sbin/nologin', '/sbin/shutdown', '/bin/false', '/bin/true']
user_ignore  = ['root']

def match(filename):
	return os.path.basename(filename) == 'passwd'

def run(filename):
	result = []
	found  = {}

	for line in readlines(filename):
		items = line.strip().split(':')
		if len(items) != 7:
			continue

		username, _, uid, gid, _, homedir, shell = items
		if shell in shell_ignore or username in user_ignore:
			continue

		found[username] = homedir

	if found:
		result.append({
			'type': 'users',
			'data': found
		})
	
	return result