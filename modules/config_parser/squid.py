# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

known_acl = [
    'localhost',
    'localnet',
    'to_localhost',
    'manager',

    'SSL_ports',
    'Safe_ports',
    'CONNECT'
]

def match(filename):
    return os.path.basename(filename).lower() == 'squid.conf'

def get_acl_white(filename):
    result = {}

    for line in readlines(filename, strip_hash = True):
        parts = re.split(r'\s+', line.strip())
        if len(parts) < 4:
            continue

        if parts[0] == 'acl' and parts[1] not in known_acl:
            if parts[1] not in result:
                result[parts[1]] = []

            result[parts[1]].append(parts[3])

    return result

def run(filename):
    acl    = get_acl_white(filename)
    result = []

    if acl:
        result.append({
            'type': 'config',
            'data': {
                'acl': acl
            }
        })
    
    return result
