# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return '.psql_history' == os.path.basename(filename)

def run(filename):
	result = []
	found  = {}

	for line in readlines(filename):
		match = re.search(r"ALTER\s+USER\s+([^\s]+)\s+with\s+password\s+'([^']+)'", line, re.I)
		if match:
			username = match.group(1).replace('"', '').replace("'", '')
			password = match.group(2).replace('"', '').replace("'", '')

			result.append({
				'type': 'credentials',
				'data': {
					'username': username,
					'password': password
				}
			})

	return result

