# -*- coding: utf-8 -*-
import re
from lxml   import etree
from pprint import pprint

xquery = "//*[local-name() = 'WindowsDeploymentServices']/*[local-name() = 'Login']/*[local-name() = 'Credentials']"

def match(filename):
	return 'unattend.xml' in filename

def run(filename):
	data   = {}
	result = []

	doc = etree.parse(filename)
	for cred in doc.xpath(xquery):
		for node in cred.getchildren():

			key = re.sub(r'.*}', '', node.tag)
			val = node.text

			if key == 'Username' or key == 'Domain' or key == 'Password':
				data[key] = val

	if len(data):
		result.append({
			'type': 'credentials',
			'data': data
		})

	return result