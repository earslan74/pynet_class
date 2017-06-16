#!/usr/bin/env python
import device_list
from napalm_base import get_network_driver
from pprint import pprint



def main():
    devices = (device_list.pynet_rtr1,)
    napalm_conns = []
    for a_device in devices:
        device_type = a_device.pop('device_type')
        merge_file = a_device.pop('merge_file')
        driver = get_network_driver(device_type)
        device = driver(**a_device)
        napalm_conns.append(device)

        print "\n>>> Test Device Open ({})".format(a_device['hostname'])
        device.open()

        print "\n>>> Rollback last config change.. "
        device.rollback()
        pprint(device.compare_config())
        print '-' * 80



if __name__ == "__main__":
    main()
