#!/usr/bin/env python
import snmp_helper
import pygal
import time

rtr1 = "184.105.247.70"

a_user = "pysnmp"
auth_key = "galileo1"
encrypt_key = "galileo1"
snmp_user = (a_user, auth_key, encrypt_key)

ifDescr_fa4 = "1.3.6.1.2.1.2.2.1.2.5"
ifInOctets_fa4 = "1.3.6.1.2.1.2.2.1.10.5"
ifInUcastPkts_fa4 = "1.3.6.1.2.1.2.2.1.11.5"
ifOutOctets_fa4 = "1.3.6.1.2.1.2.2.1.16.5"
ifOutUcastPkts_fa4 = "1.3.6.1.2.1.2.2.1.17.5"

def if_octects(interval=300, duration=3600):
    '''
    (Optionally) Takes the interval (in secs) and duration (in secs), and queries the device port in and out octects via 
    SNMPv3 every interval for the duration time.
    
    Returns 3 lists in order: if_in_octects, if_out_octects, graph_x_labels (These value lists will be used to graph 
    if_in_octects and if_out_octects via pygal)
    '''
    if_in_octects = []
    if_out_octects = []
    graph_x_labels = []
    
    snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifInOctets_fa4)
    base_in_octects = snmp_helper.snmp_extract(snmp_data)
    #print base_in_octects
    snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifOutOctets_fa4)
    base_out_octects = snmp_helper.snmp_extract(snmp_data)
    #print base_out_octects
    
    for i in range(duration/interval):
        time.sleep(interval)
        snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifInOctets_fa4)
        in_octects = snmp_helper.snmp_extract(snmp_data)
        #print in_octects
        snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifOutOctets_fa4)
        out_octects = snmp_helper.snmp_extract(snmp_data)
        #print out_octects
        if_in_octects.append(int(in_octects) - int(base_in_octects))
        #print if_in_octects
        if_out_octects.append(int(out_octects) - int(base_out_octects))
        #print if_out_octects
        base_in_octects = in_octects
        base_out_octects = out_octects

    if interval >= 60:
        for i in range(duration/interval):
            graph_val = str(((i + 1) * interval / 60.0))
            graph_x_labels.append(graph_val + "m")
    else:
        for i in range(duration/interval):
            graph_val = str(((i + 1) * interval))
            graph_x_labels.append(graph_val + "s")

    #print if_in_octects
    #print if_out_octects
    #print graph_x_labels
    return(if_in_octects, if_out_octects, graph_x_labels)


def generate_graph(if_in_octects, if_out_octects, graph_x_labels):
    '''
    Takes 3 lists as an input (if_in_octects, if_out_octects, graph_x_labels) and generates line graph in SVG format
    via pygal.
    '''
    in_out_oct = pygal.Line()
    in_out_oct.title = "Input / Output Bytes - Fa4"
    in_out_oct.add("InBytes", if_in_octects)
    in_out_oct.add("OutBytes", if_out_octects)
    in_out_oct.x_labels = graph_x_labels
    in_out_oct.render_to_file("if_bytes.svg")



def  main():
    if_in_octects, if_out_octects, graph_x_labels = if_octects(15, 300)
    generate_graph(if_in_octects, if_out_octects, graph_x_labels)
    print "Done..."







if __name__ == "__main__":
    main()
