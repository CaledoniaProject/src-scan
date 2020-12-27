# -*- coding: utf-8 -*-
import re
import os

from core.utils import unique_list, readlines

server_name_blacklist = [
	'www.lnmp.org',
	'_',
	'lnmp.org',
	'localhost'
]

allow_ip_blacklist = [
	'localhost',
	'127.0.0.1'
]

def match(filename):
	return '/nginx/' in filename or filename.endswith('.conf')

def run(filename):
	server_names = []
	allow_ips    = []
	data         = {}
	result       = []

	for line in readlines(filename, strip_hash = True):
		# 解析 allow 字段
		match = re.search(r'^\s*allow\s+(.*)\s*;', line.strip())
		if match:
			names = re.split(r'\s+', match.group(1))
			for name in names:
				if name in allow_ip_blacklist:
					continue

				allow_ips.append(name)

		# 解析 server_name 字段
		match = re.search(r'^\s*server_name\s+(.*)\s*;\s*', line.strip())
		if match:
			names = re.split(r'\s+', match.group(1))
			for name in names:
				if name in server_name_blacklist:
					continue
			
				server_names.append(name)

	if server_names:
		data['server_names'] = unique_list(server_names)
	
	if allow_ips:
		data['allow_ips']    = unique_list(allow_ips)

	if data:
		result.append({
			'type': 'config',
			'data': data
		})
	
	return result
