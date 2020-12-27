# -*- coding: utf-8 -*-

import re
import json
import xmltodict
import traceback
import base64

from core.utils import sectionToMap, cred_regex, cred_password_blacklist

def match(filename):
	return filename.endswith('.xml')

def loop(data):
	result     = []
	other      = {}

	regex_pass = cred_regex(password = True)
	regex_all  = cred_regex(all = True)

	for key, value in data.items():
		# axis2.xml
		if key == 'axisconfig':
			tmp = {}

			for parameter in value['parameter']:
				name  = parameter['@name']
				value = parameter['#text']

				if name == 'userName' or name == 'password':
					tmp[name] = value

			if 'userName' in tmp and 'password' in tmp:
				result.append({
					'type': 'credentials',
					'data': tmp
				})

		# tomcat-users.xml
		elif key == 'tomcat-users':
			tmp = {k.strip('@'): v for k, v in value['user'].items()}
			result.append({
				'type': 'credentials',
				'data': tmp
			})

			break

		# hibernate.cfg.xml
		elif key == 'hibernate-configuration' and 'session-factory' in value:
			tmp = {}

			for prop in value['session-factory']['property']:
				tmp[prop['@name']] = prop['#text']

			result.append({
				'type': 'credentials',
				'data': tmp
			})
			break

		# jdbc-driver-params
		elif key == 'jdbc-driver-params':
			tmp = {
				'url': value['url'],
			}

			if 'password-encrypted' in value:
				tmp['password-encrypted'] = value['password-encrypted']

			if type(value['properties']['property']) == list:
				for prop in value['properties']['property']:
					tmp[prop['name']] = prop['value']
			else:
				for k, v in value['properties']['property'].items():
					tmp[k] = v

			result.append({
				'type': 'credentials',
				'data': tmp
			})
			break

		# filezilla sitemanager.xml/recentservers.xml
		elif key == 'FileZilla3':
			data = []

			if 'RecentServers' in value:
				if type(value['RecentServers']['Server']) is list:
					data.extend(value['RecentServers']['Server'])
				else:
					data.append(value['RecentServers']['Server'])

			if 'Servers' in value:
				if type(value['Servers']['Server']) is list:
					data.extend(value['Servers']['Server'])
				else:
					data.append(value['Servers']['Server'])

			for Server in data:
				tmp = {
					'host': Server.get('Host'),
					'port': Server.get('Port'),
					'user': Server.get('User'),
					'pass': base64.b64decode(Server.get('Pass')['#text']).decode('utf-8'),
					'name': Server.get('Name')
				}

				result.append({
					'type': 'credentials',
					'data': tmp
				})

			break

		# JDBCConnectionPool
		elif key == 'JDBCConnectionPool':
			for prop in value:
				if '@Name' not in prop or '@PasswordEncrypted' not in prop:
					continue

				result.append({
					'type': 'credentials',
					'data': {
						'Name': prop['@Name'],
						'URL':  prop['@URL'],
						'PasswordEncrypted': prop['@PasswordEncrypted']
					}
				})

			break

		# bean
		elif key == 'bean':
			tmp = {}
			if type(value['property']) is list:
				for prop in value['property']:
					tmp[prop['@name']] = prop['@value']

				if 'username' in tmp and 'password' in tmp:
					result.append({
						'type': 'credentials',
						'data': tmp
					})

			break

		# whm
		elif key == 'admin':
			tmp = {}

			if '@user' in value and '@password' in value:
				result.append({
					'type': 'credentials',
					'data': {
						'username': value['@user'],
						'password': value['@password'],
						'admin_ips': value['@admin_ips']
					}
				})

			break

		if isinstance(value, dict):
			result.extend(loop(value))
		elif re.search(regex_all, key):
			other[key] = value

	if other:
		result.append({
			'type': 'credentials',
			'data': other
		})

	return result

def run(filename):
	result = []
	data   = None
	
	with open(filename, 'r') as f:
		data   = xmltodict.parse(f.read())
		result = loop(data)

	return result
