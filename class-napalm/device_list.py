#!/usr/bin/env python
from getpass import getpass

password = getpass()

pynet_rtr1 = dict(
	hostname='184.105.247.70',
	device_type='ios',
	username='pyclass',
	password=password,
	optional_args = {},
        merge_file='rtr1_merge.conf'
)

pynet_rtr2 = dict(
	hostname='184.105.247.71',
	device_type='ios',
	username='pyclass',
	password=password,
	optional_args = {}
)

pynet_sw1 = dict(
	hostname='184.105.247.72',
	device_type='eos',
	username='pyclass',
	password=password,
	optional_args = {}
)

pynet_sw2 = dict(
	hostname='184.105.247.73',
	device_type='eos',
	username='pyclass',
	password=password,
	optional_args = {}
)

juniper_srx = dict(
	hostname='184.105.247.76',
	device_type='junos',
	username='pyclass',
	password=password,
	optional_args = {}
)

if __name__ == "__main__":
    main()
