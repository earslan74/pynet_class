#!/usr/bin/env python
from napalm_base import get_network_driver
from pprint import pprint
import yaml


def main():
    with open("my_devices.yml", "r") as f:
        devices = yaml.load(f)

    napalm_conns = []
    for a_device in devices:
        device_type = devices[a_device].pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**devices[a_device])
        napalm_conns.append(device)

        print "\n>>> Test Device Open.."
        device.open()

        print "\n>>> Facts - Model - {} - {}: ".format(device_type, a_device),
        print device.get_facts()["model"]
        print '-' * 80

    test_methods = [
            "get_arp_table",
            "get_interfaces",
            "get_interface_ip"
    ]


if __name__ == "__main__":
    main()
