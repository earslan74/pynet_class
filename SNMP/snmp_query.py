#!/usr/bin/env python
from snmp_helper import snmp_get_oid,snmp_extract

COMMUNITY_STRING = "galileo"
SNMP_PORT = 161
SYSNAME_OID = "1.3.6.1.2.1.1.5.0"
SYSDESCR_OID = "1.3.6.1.2.1.1.1.0"

rtr1_ip = "184.105.247.70"
rtr2_ip = "184.105.247.71"

class CiscoDevice(object):
  #  COMMUNITY_STRING = "galileo" # if defined as class attributes, they need to be called from the below methods by self. notation
  #  SNMP_PORT = 161
  #  SYSNAME_OID = "1.3.6.1.2.1.1.5.0"
  #  SYSDESCR_OID = "1.3.6.1.2.1.1.1.0"
    def __init__(self, ip, hostname):
        self.ip = ip
        self.hostname = hostname
        self.vendor = "Cisco"
        self.rtr_tuple = (self.ip, COMMUNITY_STRING, SNMP_PORT)
    def sys_name(self):
        snmp_data = snmp_get_oid(self.rtr_tuple, SYSNAME_OID)
        output = snmp_extract(snmp_data)
        return output
    def sys_descr(self):
        snmp_data = snmp_get_oid(self.rtr_tuple, SYSDESCR_OID)
        output = snmp_extract(snmp_data)
        return output
        

def main():
    rtr1 = CiscoDevice(rtr1_ip, "rtr1")
    rtr2 = CiscoDevice(rtr2_ip, "rtr2")
    for device in [rtr1, rtr2]:
        print "\n" + "*" * 15 + " " + device.hostname + " " + "*" * 15        
        print "sysName: " + device.sys_name() +"\n"
        print "sysDescr: " + device.sys_descr() + "\n"

        
if __name__ == "__main__":
    main()
