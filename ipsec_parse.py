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
crypto_non_aes = ipsec_conf.find_objects_wo_child(parentspec=r"^crypto map", childspec=r"set transform-set AES")
for i in crypto_non_aes:
    print i.text.strip() + ": ",
    print i.re_search_children(r"set transform-set")[0].text.split()[-1]
 

