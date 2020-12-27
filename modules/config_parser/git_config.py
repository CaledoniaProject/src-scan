# -*- coding: utf-8 -*-
import re

from core.utils import readlines

def match(filename):
	return filename.endswith('/.git/config')

def run(filename):
	result = []

	for line in readlines(filename):
		match = re.search(r"^\s*url\s*=\s*([^\s]+)", line)
		if match is None:
			continue
		
		result.append({
			'type': 'repo',
			'data': {
				'url': match.group(1)
			}
		})

	return result
