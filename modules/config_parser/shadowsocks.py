# -*- coding: utf-8 -*-
import re
import os
import json

def match(filename):
	return os.path.basename(filename) == 'gui-config.json'

def run(filename):
	result = []
	needed = ['server', 'server_port', 'method', 'password']

	with open(filename, 'r') as f:
		data = json.load(f)

		for config in data.get('configs', []):
			valid = True

			for key in needed:
				if key not in config:
					valid = False
					break

			if valid:
				result.append({
					'type': 'credentials',
					'data': {
						'server':      config['server'],
						'server_port': config['server_port'],
						'password':    config['password'],
						'method':      config['method']
					}
				})

	return result

