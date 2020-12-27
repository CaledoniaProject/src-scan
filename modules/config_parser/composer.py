# -*- coding: utf-8 -*-
import re
import os
import json

def match(filename):
	return os.path.basename(filename) == 'auth.json'

def run(filename):
	result = []

	with open(filename, 'r') as f:
		data = json.load(f)

		if 'http-basic' in data:
			data = data['http-basic']
				
			for key, value in data.items():
				if 'username' in value and 'password' in value:
					result.append({
						'type': 'credentials',
						'data': {
							'username': value['username'],
							'password': value['password'],
							'hostname': key
						}
					})

	return result