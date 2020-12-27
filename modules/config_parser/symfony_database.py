# -*- coding: utf-8 -*-
import re
import os
import yaml

def match(filename):
    return os.path.basename(filename) == 'databases.yml'

def run(filename):
    result = []

    with open(filename, 'r') as f:
        data = yaml.safe_load(f)

        if 'all' in data and isinstance(data['all'], dict) and 'propel' in data['all']:
            propel = data['all']['propel']

            if propel['class'] == 'sfPropelDatabase':
                result.append({
                    'type': 'credentials',
                    'data': propel['param']
                })

    return result
