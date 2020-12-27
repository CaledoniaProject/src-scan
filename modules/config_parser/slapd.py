# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'slapd.conf'

def run(filename):
	result = []
	data   = {}

	for line in readlines(filename):
		match = re.search(r"^rootpw\s+({[A-Za-z]+}[^\s]+)", line)
		if match:
			data['rootpw'] = match.group(1)

		match = re.search(r'^rootdn\s+"([^"]+)"', line)
		if match:
			data['rootdn'] = match.group(1)

	if 'rootpw' in data:
		result.append({
			'type': 'credentials',
			'data': data
		})

	return result
