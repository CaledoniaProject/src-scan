# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'authorized_keys'

def run(filename):
	result = []

	for line in readlines(filename, strip_hash = True):
		parts = re.split(r'\s+', line)
		if len(parts) <= 1:
			continue

		data = {
			'type': parts[0],
			'key':  parts[1]
		}

		if len(parts) == 3:
			data['name'] = parts[2]

		result.append({
			'type': 'authorized_keys',
			'data': data
		})

	return result
