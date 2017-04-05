#!/usr/bin/env python
import json, yaml
from pprint import pprint as pp

yaml_file = "dev_param.yml"
json_file = "dev_param.json"
print "\n******** YAML FILE **********"
with open(yaml_file, "r") as f:
    my_list = yaml.load(f)
pp (my_list)

print "\n******** JSON FILE ***********"
with open(json_file, "r") as f:
    my_list = json.load(f)
pp (my_list)

