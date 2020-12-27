# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
	return True

def run(filename):
	result = []
	data   = {}

	for line in readlines(filename):
		match = re.search(r"^enable\s+(password|secret)\s*[0-9]\s*(.*)", line)
		if match:
			data[match.group(1)] = match.group(2)

	if data:
		result.append({
			'type': 'credentials',
			'data': data
		})

	return result
