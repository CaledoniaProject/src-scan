# -*- coding: utf-8 -*-
import re
import traceback
import configparser

from modules.config_parser import winscp
from core.utils            import sectionToMap, cred_regex, cred_password_blacklist, read_ini

def match(filename):
	return filename.endswith('.ini') and not winscp.match(filename)

def run(filename):
	result     = []
	Config     = read_ini(filename)

	regex_pass = cred_regex(password = True)
	regex_all  = cred_regex(all = True)

	for section in Config.sections():
		tmp      = {}
		has_pass = False

		for key, value in sectionToMap(Config, section).items():
			if not value or len(value.strip()) == 0:
				continue
			
			if cred_password_blacklist(value):
				continue
					
			if re.search(regex_all, key, re.IGNORECASE):
				tmp[key] = value
			if re.search(regex_pass, key, re.IGNORECASE):
				has_pass = True

		if has_pass:
			result.append({
				'type': 'credentials',
				'data': tmp
			})			

	return result
