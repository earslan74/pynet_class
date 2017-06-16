#!/usr/bin/env python
import device_list
from napalm_base import get_network_driver
from pprint import pprint



def main():
    devices = (device_list.pynet_rtr1,
            device_list.pynet_rtr2,
            device_list.pynet_sw1,
            device_list.pynet_sw2,
            device_list.juniper_srx
    )
    napalm_conns = []
    for a_device in devices:
        device_type = a_device.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**a_device)
        napalm_conns.append(device)

        print "\n\n>>> Test Device Open.."
        device.open()

        print "\n>>> Facts  - Model {} {}: ".format(device_type, a_device['hostname']),
        print device.get_facts()["model"]
        print '-' * 80


    test_methods = [
            "get_arp_table",
            "get_interfaces",
            "get_interface_ip"
    ]


if __name__ == "__main__":
    main()
