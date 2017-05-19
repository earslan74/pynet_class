#!/usr/bin/env python
import pyeapi



def main():
    pynet_sw1 = pyeapi.connect_to("pynet-sw1")
    show_if = pynet_sw1.enable("show interfaces")
    interfaces = show_if[0]["result"]["interfaces"]
    print "******** Switch Interface Counters ********\n"
    for intf in interfaces:
        if intf.startswith("Vlan"):
            continue
        else:
            print intf + " >>> ",
            print "  InOctets:",
            print interfaces[intf]["interfaceCounters"]["inOctets"], 
            print "  OutOctets:",
            print interfaces[intf]["interfaceCounters"]["outOctets"]
    print "\n"    

if __name__ == "__main__":
    main()
