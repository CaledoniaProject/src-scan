# -*- coding: utf-8 -*-

import re
import os
import string
import configparser
import chardet

from cryptography import x509, hazmat

def read_ini(filename):
    config = configparser.ConfigParser(strict = False)
    
    try:
        config.read(filename)
    except configparser.MissingSectionHeaderError:
        with open(filename, 'r') as f:
            config.read_string("[dummy]\n" + f.read())

    return config

def is_binary_file(filename):
    if not os.path.isfile(filename):
        return True

    try:
        for line in readlines(filename):
            continue

        return False
    except:
        pass

    return True

def readlines(filename, **kwargs):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if 'strip_hash' in kwargs and line.startswith('#'):
                continue

            yield line.strip()

def get_cert_subject(filename):
    result  = None
    backend = hazmat.backends.default_backend()

    with open(filename, 'rb') as myfile:
        data = myfile.read()

    cert = x509.load_pem_x509_certificate(data, backend)
    for attr in cert.subject:
        # 2.5.4.3: commonName
        if attr.oid.dotted_string == '2.5.4.3':
            result = attr.value
            break

    return result

def is_sshkey_encrypted(filename):
	with open(filename, 'r') as f:
		data = f.read()

	return 'Proc-Type:' in data

def load_properties(filepath, sep='=', comment_char='#'):
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value
    return props

def sectionToMap(Config, section):
    dict1   = {}
    options = Config.options(section)

    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            dict1[option] = None

    return dict1

def cred_regex(**kwargs):
    result     = []

    _username  = [
        'username', 'user', 'usr', 'login', 'user-name', 'user_name',
        'LDAP_BIND_DN', 
        'mailFrom', 'address'
    ]

    _password  = [
        'passwd', 'password', 'pass', 'pwd', 'pswd', 'auth', 'pw'
    ]

    _host      = [
        'url', 'host', '\\bip\\b', 'server', 'dbname',
        'SQLALCHEMY_DATABASE_URI'
    ]

    _accesskey = [
    	'uc_key', 'uc_api',
        'api_key', 'apikey', 
        'access_key', 'access_id', 'aliyun_bucket',
        'secret_key'
    ]

    if 'username' in kwargs or 'all' in kwargs:
        result.extend(_username)
    if 'password' in kwargs or 'all' in kwargs:
        result.extend(_password)
    if 'host' in kwargs or 'all' in kwargs:
        result.extend(_host)
    if 'accesskey' in kwargs or 'all' in kwargs:
        result.extend(_accesskey)

    return '(' + '|'.join(result) + ')'

def cred_password_blacklist(value):
    if value == 'true':
        return True

    return False

def unique_list(l):
    return list(set(l))

def strip_quotes(s):
    return re.sub(r'["\']', '', s)


