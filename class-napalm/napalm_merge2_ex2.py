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

        print "\n>>> Load config change (merge) - with commit.. "
        device.load_merge_candidate(filename=merge_file)
        pprint(device.compare_config())
        print
        raw_input('Hit Enter to commit changes: ')

        print "\n>>> Commit config change (merge)"
        device.commit_config()
        pprint(device.compare_config())
        print '-' * 80



if __name__ == "__main__":
    main()
