# -*- coding: utf-8 -*-
import re
import os
import traceback
import configparser

from core.utils  import sectionToMap, strip_quotes

def match(filename):
	return os.path.basename(filename) == '.pypirc'

def run(filename):
	result = []
	Config = configparser.ConfigParser(allow_no_value = True, strict = False)

	Config.read(filename)

	for section in Config.sections():
		data = sectionToMap(Config, section)

		if 'password' in data and 'username' in data:
			tmp = {
				'username': data['username'],
				'password': data['password']
			}

			if 'repository' in data:
				tmp['repository'] = data['repository']

			result.append({
				'type': 'credentials',
				'data': tmp
			})

	return result


