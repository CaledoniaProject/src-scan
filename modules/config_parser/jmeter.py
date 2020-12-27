# -*- coding: utf-8 -*-
import re
from lxml   import etree
from pprint import pprint

def match(filename):
	return filename.endswith('.jmx')

def run(filename):
	result = []
	attrs  = {}

	doc = etree.parse(filename)
	for df in doc.xpath('//AuthManager/collectionProp/elementProp/stringProp'):
		if 'name' in df.attrib and df.text is not None:
			attrs[df.attrib['name'].replace('Authorization.', '')] = df.text

	if 'url' in attrs and 'username' in attrs and 'password' in attrs:
		result.append({
			'type': 'credentials',
			'data': {
				'url':      attrs['url'],
				'username': attrs['username'], 
				'password': attrs['password']
			}
		})

	return result