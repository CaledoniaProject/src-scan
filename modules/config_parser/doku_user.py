# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'users.auth.php'

def run(filename):
	result = []
	tmp    = {}

	for line in readlines(filename, strip_hash = True):
		parts = line.split(':')
		if len(parts) != 5:
			continue
		
		result.append({
			'type': 'credentials',
			'data': {
				'username': parts[0],
				'password': parts[1],
				'realname': parts[2],
				'email':    parts[3],
				'group':    parts[4]
			}
		})			

	return result
