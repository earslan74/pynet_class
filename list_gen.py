#!/usr/bin/env python
import yaml, json
from pprint import pprint as pp
dev_list = []
attribs = {}
yml_file = "dev_param.yml"
json_file = "dev_param.json"

ip_list = raw_input("Enter IP addresses of the devices (comma separated): ").replace(" ", "").split(",")
attribs["vendor"] = raw_input("Device Vendor: ").strip()
attribs["model"] = raw_input("Device Model: ").strip()
attribs["dns"] = raw_input("DNS Servers (comma separated): ").replace(" ", "").split(",")
attribs["ntp"] = raw_input("NTP Servers (comma separated): ").replace(" ", "").split(",")
attribs["syslog"] = raw_input("Syslog Servers (comma separated): ").replace(" ", "").split(",") 

for i in ip_list:
    dev_list.append(i)
dev_list.append(attribs)
pp (dev_list)

with open(yml_file, "w") as f:
    print "Saving in {0} file in YAML format.".format(yml_file)
    f.write(yaml.dump(dev_list, default_flow_style=False))
with open(json_file, "w") as f:
    print "Saving in {0} file in JSON format".format(json_file)
    json.dump(dev_list, f)


