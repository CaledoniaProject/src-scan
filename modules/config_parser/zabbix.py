# -*- coding: utf-8 -*-
import re
import os
import traceback

from core.utils import sectionToMap, readlines

def match(filename):
	filename = os.path.basename(filename)
	return filename == 'zabbix_server.conf' or filename == 'zabbix_proxy.conf'

def run(filename):
	tmp    = {'DBHost': 'localhost', 'DBPort': 3306}
	result = []
	wanted = ['DBHost', 'DBName', 'DBUser', 'DBPassword', 'DBPort']

	for line in readlines(filename):
		parts = re.split(r'\s*=\s*', line.strip())
		if parts[0] in wanted:
			tmp[parts[0]] = parts[1]

	if len(tmp) == 5:
		result.append({
			'type': 'credentials',
			'data': tmp
		})
	return result