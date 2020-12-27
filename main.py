#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
import argparse

from core.loggers import log
from modules      import config_parser

sys.dont_write_bytecode = True

def group_data(data, field):
	result = {}

	for row in data:
		type_ = row[field]
		if type_ not in result:
			result[type_] = []

		del row[field]
		result[type_].append(row)

	return result

def run(path, args):
	if not os.path.exists(path):
		return []

	path = os.path.realpath(path)
		
	# 最大文件大小
	size = os.path.getsize(path)
	if size > args.maxsize * 1024 * 1024:
		log.debug("Skipped %s (%d bytes)", path, size)
		return []

	result = config_parser.run(path, args)
	return result

def walk_dir(path, args):
	result = []

	try:
		for root, subdirs, files in os.walk(path):
			# 处理文件
			for file in files:
				result.extend(run (root + '/' + file, args))
	except KeyboardInterrupt:
		print ("\n")
		pass

	return result

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('dir', 
		metavar = 'files', type = str, nargs = '*',
		help = 'Directory or files to scan')
	parser.add_argument('--disable', 
		default = [], required = False, nargs = '+', dest = "disable", 
		help = 'Modules to disable')
	parser.add_argument('--maxsize',
		default = 2, required = False, type = int, dest = "maxsize", 
		help = 'Maximum allowed file size (MB)')
	parser.add_argument('--encoding',
		default = "utf8", required = False, dest = "encoding", 
		help = 'Specify encoding')
	parser.add_argument('--raw',
		default = False, required = False, dest = "raw", action = 'store_true',
		help = 'Print raw python structure')

	args   = parser.parse_args()
	result = []

	if len(args.dir) == 0:
		# print ('No arguments provided, scanning', os.getcwd(), "\n")
		result.extend(walk_dir (os.getcwd(), args))
	else:		
		for target in args.dir:
			if os.path.isdir(target):
				result.extend(walk_dir(target, args))
			else:
				result.extend(run (target, args))

	if args.raw:
		tmp = []
		for row in result:
			del(row['filename'])
			del(row['module'])
			
			tmp.append(row)

		print(tmp)
	else:	
		# 也可以用 type 分组
		result = group_data(result, 'module')
		print(json.dumps(result))
