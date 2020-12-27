import os
import copy
import json
import socket
import logging
import logging.handlers

def get_handler(filename, console = False):
    log_path     = filename
    formatter    = logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)d %(funcName)s] %(message)s',
        '%Y-%m-%d %H:%M:%S')

    file_handler = logging.handlers.RotatingFileHandler(
        log_path,
        mode        = 'a',
        maxBytes    = 10 * 1024 * 1024,
        backupCount = 2,
        encoding    = None,
        delay       = 0
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    return file_handler

filename = '/tmp/src-scan.log'
if os.path.exists(filename):
    os.remove(filename)

log = logging.getLogger('log')
log.addHandler(get_handler(filename))
log.setLevel(logging.DEBUG)
