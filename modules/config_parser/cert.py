# -*- coding: utf-8 -*-
import os

from core.utils import get_cert_subject

bad_commonNames = [
    'imap.example.com',
    'Entrust.net Secure Server Certification Authority',

    # cpan Net-SSLeay-1.55
    'simple.server.cert',
    'extended.server.cert',
    '127.0.0.1'
]

def match(filename):
    return filename.endswith('.pem') or filename.endswith('.cert')

def run(filename):
    commonName = get_cert_subject(filename)

    if commonName is None or commonName in bad_commonNames:
        return []

    if '.' not in commonName:
        return []

    return [{
        'type': 'certificate',
        'data': {
            'commonName': commonName
        }
    }]
