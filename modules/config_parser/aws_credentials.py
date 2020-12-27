# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'credentials'

def run(filename):
	tmp    = {}
	result = []

	for line in readlines(filename):
		match = re.search(r'([^\s]+)\s*=[\s"]*([^\s"]+)', line.strip())
		if not match:
			continue

		name  = match.group(1)
		value = match.group(2)

		if name in ['aws_access_key_id', 'aws_secret_access_key']:
			tmp[name] = value

	if 'aws_secret_access_key' in tmp and 'aws_access_key_id' in tmp:
		result.append({
			'type': 'credentials',
			'data': tmp
		})

	return result