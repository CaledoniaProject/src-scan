# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return '/.lftp/rl_history' in filename

def run(filename):
	tmp    = {}
	result = []

	for line in readlines(filename):
		# lftp ftp://user:pass@hostname
		match = re.search(r"^lftp\s+ftps?:\/\/.*", line)
		if match:
			tmp[line] = True

	if len(tmp):
		result.append({
			'type': 'history',
			'data': {'lftp': list(tmp.keys())}
		})
	
	return result