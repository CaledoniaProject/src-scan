# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

blacklist = [
	'::1',
	'127.0.0.1',
	'255.255.255.255'
]

def match(filename):
	return filename.endswith('/etc/hosts')

def run(filename):
	hosts  = {}
	result = []

	for line in readlines(filename, strip_hash = True):
		line  = re.sub(r'\s*#.*', '', line)
		parts = re.split(r'\s+', line)

		if parts[0] in blacklist:
			continue

		hosts[parts[0]] = parts[1:]

	if hosts:
		result.append({
			'type': 'hosts',
			'data': hosts
		})
	
	return result