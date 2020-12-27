# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

progs = [
	'su', 'sudo', 
	'ssh', 'scp', 'sftp', 'ssh-copy-id', 'telnet',
	'ftp', 'lftp', 
	'mysql', 'mysqldump', 'psql', 'sqlite3', 'sqlcipher',
	'rsync', 
	'wget', 'curl',
	'ldapsearch', 
	'crontab',
	'sshpass',
	'git', 'svn', 'pmm-admin'
]

keywords = [
	r'curl.*X-Auth-Key',
	r'\|\s*md5sum',
	r'\.psa\.shadow'
]

def match(filename):
	name    = os.path.basename(filename)
	allowed = ['bash_history', '.bash_history', 'zsh_history', '.zsh_history']
	return name in allowed or name.endswith('.sh')

def run(filename):
	tmp    = {}
	result = []

	for line in readlines(filename):
		items = re.split(r'\s+', line)

		# 非通用的
		for keyword in keywords:
			if re.search(keyword, line):
				if items[0] not in tmp:
					tmp[items[0]] = {}
						
				tmp[items[0]][line] = True
				break

		# 通用的
		for prog in progs:		
			items[0] = re.sub(r'.*/', '', items[0])

			if items[0] == prog:					
				# 除了 su，别的如果不带参数都没有意义
				if prog != 'su' and len(items) == 1:
					continue

				if items[0] not in tmp:
					tmp[items[0]] = {}

				tmp[items[0]][line] = True

	for k, v in tmp.items():
		tmp[k] = list(v.keys())

	if len(tmp):
		result.append({
			'type': 'history',
			'data': tmp
		})

	return result