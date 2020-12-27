# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'wp-config.php'

def run(filename):
	data    = {}
	result  = []
	mapping = {
		'DB_NAME':     'database',
		'DB_USER':     'username',
		'DB_PASSWORD': 'password',
		'DB_HOST':     'hostname'
	}

	for line in readlines(filename):
		match = re.search(r"define.*'([^']+)'.*'([^']+)'", line)
		if not match:
			continue

		key   = match.group(1)
		value = match.group(2)

		if key in mapping:
			data[ mapping[key] ] = value

	if 'username' in data and 'password' in data:
		result.append({
			'type': 'credentials',
			'data': data
		})

	return result