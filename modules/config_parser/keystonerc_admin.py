# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

def match(filename):
    return os.path.basename(filename) == 'keystonerc_admin'

def run(filename):
    data   = {}
    wanted = ['OS_USERNAME', 'OS_PASSWORD', 'OS_AUTH_URL']
    result = []

    for line in readlines(filename):
        match = re.search(r"^\s*export (OS_[^\s]+)=([^\s]+)", line)
        if not match:
            continue
        
        key   = match.group(1)
        value = match.group(2)

        if key in wanted:
            data[key] = value

    if len(wanted) == len(data):
        result.append({
            'type': 'credentials',
            'data': data
        })

    return result