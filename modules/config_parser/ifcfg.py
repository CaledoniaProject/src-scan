# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	basename = os.path.basename(filename)
	return basename.startswith('ifcfg-') and basename != 'ifcfg-lo'

def run(filename):
	result = []
	tmp    = {}

	for line in readlines(filename, strip_hash = True):
		parts = line.split('=')
		if len(parts) == 2:
			tmp[parts[0]] = parts[1].replace('"', '')

	if 'IPADDR' in tmp and 'NETMASK' in tmp:
		result.append({
			'type': 'config',
			'data': {
				'address': tmp['IPADDR'],
				'netmask': tmp['NETMASK']
			}
		})	

	return result
