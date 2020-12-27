# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'redis.conf'

def run(filename):
	result = []

	for line in readlines(filename):
		match = re.search(r"(masterauth|requirepass)\s+(.*)", line)
		if match:
			result.append({
				'type': 'credentials',
				'data': {
					match.group(1): match.group(2)
				}
			})

	return result
