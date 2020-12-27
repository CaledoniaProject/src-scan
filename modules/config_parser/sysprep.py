# -*- coding: utf-8 -*-
import re
import os
import configparser

from pprint       import pprint
from core.utils  import sectionToMap

def match(filename):
	return 'sysprep.inf' == os.path.basename(filename)

def run(filename):
	result = []
	Config = configparser.ConfigParser(strict = False)

	Config.read(filename)

	for section in Config.sections():
		if section == 'GuiUnattended':
			data = sectionToMap(Config, section)
			if 'adminpassword' in data:
				password = data['adminpassword']

				if password.startswith('"') and password.endswith('"'):
					password = password[1:-1]

				result.append({
					'type': 'credentials',
					'data': {
						'user':    'administrator',
						'password': password
					}
				})

	return result
