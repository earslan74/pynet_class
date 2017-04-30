#!/usr/bin/env python
from getpass import getpass

password = getpass()

pynet1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': password
}
pynet2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': password
}
juniper_srx = {
    'device_type': 'juniper',
    'ip': '184.105.247.76',
    'username': 'pyclass',
    'password': password,
    'secret': ''
}
