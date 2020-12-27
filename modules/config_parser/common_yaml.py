# -*- coding: utf-8 -*-
import re
import os
import yaml
import types

from core.utils import cred_regex, load_properties
from modules.config_parser import symfony_database

def match(filename):
	if symfony_database.match(filename):
		return False

	return filename.endswith(".yaml") or filename.endswith(".yml")

# 深度递归
def loop(data):
	regex  = cred_regex(username = True, password = True, accesskey = True)
	result = []
	tmp    = {}

	if isinstance(data, dict):
		for key, value in data.items():
			if isinstance(value, str) and re.search(regex, key):
				tmp[key] = value

			if type(value) is dict:
				result.extend(loop(value))

	if tmp:
		result.append({
			'type': 'credentials',
			'data': tmp
		})

	return result

def run(filename):
	props  = load_properties(filename)
	result = []

	with open(filename, 'r') as f:
		data   = yaml.safe_load(f)
		result = loop(data)
	
	return result
