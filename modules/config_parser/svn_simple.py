# -*- coding: utf-8 -*-
import re
import os

from core.utils import readlines

columns = ['password', 'server', 'username']

def match(filename):
    return 'svn.simple/' in filename

def run(filename):
    data  = {}
    lines = list(readlines(filename))

    for i in range(0, len(lines) - 1, 4):
        key   = lines[i + 1]
        value = lines[i + 3]

        if key == 'svn:realmstring':
            match = re.search(r"<([^>]+)>", value)
            if match:
                value = match.group(1)

            key = 'server'

        data[key] = value

    for column in columns:
        if column not in data:
            return []

    return [{
        'type': 'credentials',
        'data': data
    }]


