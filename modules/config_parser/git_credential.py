# -*- coding: utf-8 -*-

import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == '.git-credentials'

def run(filename):
	data   = []
	result = []

	for line in readlines(filename):
		match = re.search(r'.*://(.*):(.*)@(.*)', line)
		if match:
			data.append(line)

	if data:
		result.append({
			'type': 'credentials',
			'data': { 'credentials': data }
		})

	return result