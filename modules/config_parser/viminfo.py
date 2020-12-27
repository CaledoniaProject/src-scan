# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == '.viminfo'

def run(filename):
	files  = []
	found  = {}
	result = []

	for line in readlines(filename):
		if line.startswith('> '):
			name = line[2:]

			if name not in found:
				found[name] = True
				files.append(name)

	if len(files):
		result.append({
			'type': 'history',
			'data': {'files': files}
		})
	
	return result