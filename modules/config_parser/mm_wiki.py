# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'mm-wiki.conf'

def run(filename):
	data   = {}
	result = []

	for line in readlines(filename):
		match = re.search(r'^(host|user|pass|name)="([^"]+)"', line.strip())
		if match:
			data[match.group(1)] = match.group(2)

	if len(data) == 4:
		result.append({
			'type': 'credentials',
			'data': data
		})
	
	return result