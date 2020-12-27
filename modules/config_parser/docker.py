# -*- coding: utf-8 -*-
import re
import os
import json

from core.utils import readlines

def match(filename):
	return filename.endswith('/.docker/config.json')

def run(filename):
	result = []
	data   = {}

	with open(filename, 'r') as f:
		data = json.loads(f.read())

	if 'auths' in data:
		for key, value in data['auths'].items():
			value['url'] = key
			result.append({
				'type': 'credentials',
				'data': value
			})
			
	return result