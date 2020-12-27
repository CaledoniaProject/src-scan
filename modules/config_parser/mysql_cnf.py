# -*- coding: utf-8 -*-
import re
import os
import configparser

from pprint     import pprint
from core.utils import sectionToMap, strip_quotes, read_ini

def match(filename):
	return '.cnf' in os.path.basename(filename)

def run(filename):
	result = []
	Config = read_ini(filename)

	for section in Config.sections():
		data = sectionToMap(Config, section)

		# MySQL client password
		if 'password' in data:
			tmp = {'password': data['password']}

			if 'host' in data:
				tmp['hostname'] = data['host']
			if 'user' in data:
				tmp['username'] = data['user']

			result.append({
				'type': 'credentials',
				'data': tmp
			})

		# galera cluster
		if 'wsrep_sst_auth' in data and ':' in data['wsrep_sst_auth']:
			parts = data['wsrep_sst_auth'].strip().split(':')
			tmp   = {
				'username': parts[0],
				'password': parts[1]
			}

			if 'wsrep_node_address' in data:
				tmp['hostname'] = data['wsrep_node_address']
			if 'wsrep_node_name' in data:
				tmp['nodename'] = strip_quotes(data['wsrep_node_name'])

			result.append({
				'type': 'credentials',
				'data': tmp
			})

	return result
