#!/usr/bin/env python

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from getpass import getpass
from pprint import pprint




def main():
    pwd = getpass()
    a_device = Device(host='184.105.247.76', user='pyclass', password=pwd)
    a_device.open()
    print "\n***** Device Facts *****\n"
    pprint (a_device.facts)
    print "\n***** Config Change...****\n"
    cfg = Config(a_device)
    cfg.lock()
    print "Config is locked..."
    cfg.load(path='srx_hostname.conf', format='text', merge=True)
    print "Config change is uploaded.."
    cfg.pdiff()

    answer = raw_input("Do you want to rollback(y/n): ")
    if answer in ['y', 'Y', 'yes', 'YES']:
        print "Rollback is in progress..."
        cfg.rollback(0)
        cfg.commit()
        cfg.pdiff()
    else:
        pass

    cfg.unlock()

if __name__ == "__main__":
    main()

