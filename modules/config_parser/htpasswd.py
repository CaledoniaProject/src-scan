# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) in ['.htpasswd', 'htpasswd']

def run(filename):
	result = []

	for line in readlines(filename):
		items = line.strip().split(':')
		if len(items) != 2:
			continue
			
		result.append({
			'type': 'credentials',
			'data': {
				'username': items[0], 
				'password': items[1]
			}
		})
			
	return result

