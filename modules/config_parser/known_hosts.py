# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return 'known_hosts' == os.path.basename(filename)

def run(filename):
	tmp    = []
	result = []

	for line in readlines(filename):
		items = line.split(' ')

		if len(items) == 3 and not items[0].startswith('|1|'):
			tmp.append(items[0])

	if len(tmp):
		result.append({
			'type': 'config',
			'data': {'hosts': tmp}
		})

	return result


