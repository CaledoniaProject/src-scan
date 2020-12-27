# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return 'rsync' in os.path.basename(filename)

def run(filename):
	result  = []
	section = None

	for line in readlines(filename, strip_hash = True):
		# [section]
		match = re.search(r"^\[([^\]]+)\]$", line)
		if match:
			section = match.group(1)

		match = re.search(r"secrets file\s*=\s*(.*)", line)
		if match and section:
			result.append({
				'type': 'config',
				'data': {
					'secrets': match.group(1),
					'section': section
				}
			})

	return result