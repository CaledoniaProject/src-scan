# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return True

def run(filename):
	result = []

	for line in readlines(filename):
		match = re.search(r"['\" ]mysql://(.*):(.*)@([^/]+)/(\w+)['\" ]", line)
		if match is None:
			continue
		
		data = {
			'username':	match.group(1),
			'password': match.group(2),
			'hostname': match.group(3),
			'database': match.group(4)
		}
		
		result.append({
			'type': 'credentials',
			'data': data
		})

	return result