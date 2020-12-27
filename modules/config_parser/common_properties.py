# -*- coding: utf-8 -*-
import re
import os

from core.utils import cred_regex, load_properties, cred_password_blacklist

def match(filename):
	return os.path.basename(filename).endswith(".properties")

def run(filename):
	result     = []
	tmp        = {}

	regex_pass = cred_regex(password = True)
	regex_all  = cred_regex(all = True)

	for key, value in load_properties(filename).items():
		namespace = ''

		if '@' in key:
			namespace = key.rsplit('@', 2)[1]
		else:
			namespace = key.rsplit('.', 2)[0] if '.' in key else ''

		if namespace not in tmp:
			tmp[namespace] = {'data': {}, 'has_pass': False}

		if cred_password_blacklist(value):
			continue

		if re.search(regex_all, key, re.IGNORECASE):
			tmp[namespace]['data'][key] = value
		if re.search(regex_pass, key, re.IGNORECASE):
			tmp[namespace]['has_pass']  = True
	
	for namespace, item in tmp.items():
		if item['has_pass']:
			result.append({
				'type': 'credentials',
				'data': item['data']
			})

	return result
