# -*- coding: utf-8 -*-
import re
import os
from urllib.parse import urlparse

from core.utils import readlines

def match(filename):
	return os.path.basename(filename) == 'Podfile'

def run(filename):
	result = []

	for line in readlines(filename):
		match = re.search(r'git:\s*"(.*)"', line)
		if match is None:
			continue
		
		urlobj = urlparse(match.group(1))
		if urlobj.username and urlobj.password:
			result.append({
				'type': 'credentials',
				'data': {
					'username': urlobj.username,
					'password': urlobj.password
				}
			})

	return result

