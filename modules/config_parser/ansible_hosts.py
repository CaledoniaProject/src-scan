# -*- coding: utf-8 -*-
import re
import traceback
import configparser

from core.utils import sectionToMap, readlines

def match(filename):
    return filename.endswith('/ansible/hosts')

def run(filename):
    result = []

    result.extend(run_vars(filename))
    result.extend(run_lines(filename))

    return result

def run_vars(filename):
    result = []
    Config = configparser.ConfigParser(allow_no_value = True)
    Config.read(filename)

    for section in Config.sections():
        data = sectionToMap(Config, section)

        if not section.endswith(':vars'):
            continue
            
        if 'ansible_ssh_pass' in data and 'ansible_ssh_user' in data:
            tmp = {
                'ssh_host':  '',
                'ssh_user':  data['ansible_ssh_user'],
                'ssh_pass':  data['ansible_ssh_pass'],
                'ssh_port':  22
            }

            if 'ansible_ssh_port' in data:
                tmp['ssh_port'] = data['ansible_ssh_port']

            name = section.replace(':vars', '')
            if name in Config.sections():
                tmp['ssh_host'] = Config.options(name)

            result.append({
                'type': 'credentials',
                'data': tmp
            })

    return result

def run_lines(filename):
    result = []
    group  = ''

    for line in readlines(filename):
        if line.startswith('[') and line.endswith(']'):
            group = line.strip(']').strip('[')
            continue

        parts = re.split(r'\s+', line)
        tmp   = {
            'ssh_group': group,
            'ssh_host':  parts[0],
            'ssh_user':  None,
            'ssh_pass':  None,
            'ssh_port':  22
        }

        for part in parts:
            match = re.search(r'ansible_(ssh_[a-z]+)=(.*)', part)
            if match:
                tmp[match.group(1)] = match.group(2)

        if tmp['ssh_pass'] and tmp['ssh_user']:
            result.append({
                'type': 'credentials',
                'data': tmp
            })

    return result




