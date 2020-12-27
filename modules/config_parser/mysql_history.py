# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == '.mysql_history'

def run(filename):
	result = []
	found  = {}

	for line in readlines(filename):
		match = re.search(r"GRANT.*ON\s+([^\s]+)\s+TO\s+([^\s]+)\s+IDENTIFIED.*BY.*['\"]([^'\"]+)['\"]", line, re.I)
		if match:
			database = match.group(1).replace('"', '').replace("'", '')
			username = match.group(2).replace('"', '').replace("'", '')
			password = match.group(3).replace('"', '').replace("'", '')

			result.append({
				'type': 'credentials',
				'data': {
					'database': database,
					'username': username, 
					'password': password
				}
			})

	return result