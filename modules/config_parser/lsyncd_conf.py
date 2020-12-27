# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'lsyncd.conf'

def run(filename):
	tmp    = {}
	result = []

	for line in readlines(filename):
		# password_file = XX
		match = re.search(r'([^\s]+)\s*=\s*"([^"]+)"', line.strip())
		if not match:
			continue

		name  = match.group(1)
		value = match.group(2)

		if name in ['password_file', 'target', 'source']:
			tmp[name] = value

	if 'password_file' in tmp and 'target' in tmp:
		result.append({
			'type': 'credentials',
			'data': tmp
		})

	return result