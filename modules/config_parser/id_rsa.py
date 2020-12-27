# -*- coding: utf-8 -*-
import re
import os

from core.utils import is_sshkey_encrypted

def match(filename):
	return os.path.basename(filename) == 'id_rsa'

def run(filename):
	result = []
	if not is_sshkey_encrypted(filename):
		result.append({
			'type': 'ssh_private_key',
			'data': {
				'ssh-key': 'No password protection'
			}
		})

	return result
