# -*- coding: utf-8 -*-
import re
import os

from lxml import etree

def match(filename):
	return os.path.basename(filename) == 'web.config'

def run(filename):
	result = []
	data   = []

	doc = etree.parse(filename)
	for df in doc.xpath('//connectionStrings/add'):
		if 'connectionString' in df.attrib:
			data.append(df.attrib['connectionString'])

	if len(data):
		result.append({
			'type': 'credentials',
			'data': {'connectionStrings': data}
		})
	
	return result