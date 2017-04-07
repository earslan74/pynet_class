#!/usr/bin/env python
from ciscoconfparse import CiscoConfParse

ipsec_conf = CiscoConfParse("cisco_ipsec.txt")
# Find all the "crypto map CRYPTO" entries
crypto = ipsec_conf.find_objects(r"^crypto\smap\sCRYPTO")
# Print the children of each crypto map entry
print "****** Crypto map CRYPTO Config ******\n"
for i in crypto:
    print i.text
    for j in i.children:
        print j.text
    print "!"

print "\n***** Crypto Maps Using PFS Group2 ****\n"
#pfs2_maps = ipsec_conf.find_objects_w_child(parentspec=r"^crypto map", childspec=r"^ set pfs group2")
#for i in pfs2_maps:
#    print i.text
for c_map in crypto:
    if c_map.has_child_with(r"^ set pfs group2"):
        print c_map.text

print "\n***** Non-AES Crypto Maps *****\n"
for i in ipsec_conf.find_objects_wo_child(parentspec=r"^crypto map", childspec=r"^ set transform-set AES"):
    print i.text + ": ",
    print i.find_children(r"^ set transform-set").text.split()[-1]
 

