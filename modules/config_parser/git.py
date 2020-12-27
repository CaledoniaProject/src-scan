# -*- coding: utf-8 -*-

import re
import os
import subprocess

from os.path import dirname, realpath

def match(filename):
	return filename.endswith('/.git/config')

def is_free_mailaddress(author):
	return '@gmail.com' in author or '@googlemail.com' in author

def run(filename):
	emails   = {}
	free_cnt = 0
	rootpath = realpath(dirname(filename) + '/../')

	p = subprocess.Popen(['git', 'log'], cwd = rootpath, stdout = subprocess.PIPE, 
				                                   	 stderr = subprocess.PIPE)

	out, err = p.communicate()

	for line in out.decode('utf8').split("\n"):
		match = re.search(r"^Author: .*<(.*)>", line)
		if match:
			author = match.group(1)

			if is_free_mailaddress(author) and author not in emails:
				free_cnt += 1

			emails[author] = True

	if len(emails) == 0 or free_cnt >= 5:
		return []
	else:
		return [{
			'type': 'email',
			'data': { 
				'emails': list(emails.keys())
			} 
		}]
