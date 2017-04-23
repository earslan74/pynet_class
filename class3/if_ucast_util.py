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

def if_ucast_pkts(interval=300, duration=3600):
    '''
    (Optionally) Takes the interval (in secs) and duration (in secs), and queries the device port for in and out unicast
    packets via SNMPv3 every interval for the duration time.
    
    Returns 3 lists in order: if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels (These value lists will be used to 
    graph if_in_ucast_pkts and if_out_ucast_pkts via pygal)
    '''
    if_in_ucast_pkts = []
    if_out_ucast_pkts = []
    graph_x_labels = []
    
    snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifInUcastPkts_fa4)
    base_in_ucast_pkts = snmp_helper.snmp_extract(snmp_data)
    print base_in_ucast_pkts
    snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifOutUcastPkts_fa4)
    base_out_ucast_pkts = snmp_helper.snmp_extract(snmp_data)
    print base_out_ucast_pkts
    
    for i in range(duration/interval):
        time.sleep(interval)
        snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifInUcastPkts_fa4)
        in_ucast_pkts = snmp_helper.snmp_extract(snmp_data)
        print in_ucast_pkts
        snmp_data = snmp_helper.snmp_get_oid_v3((rtr1, 161), snmp_user, oid=ifOutUcastPkts_fa4)
        out_ucast_pkts = snmp_helper.snmp_extract(snmp_data)
        print out_ucast_pkts
        if_in_ucast_pkts.append(int(in_ucast_pkts) - int(base_in_ucast_pkts))
        print if_in_ucast_pkts
        if_out_ucast_pkts.append(int(out_ucast_pkts) - int(base_out_ucast_pkts))
        print if_out_ucast_pkts
        base_in_ucast_pkts = in_ucast_pkts
        base_out_ucast_pkts = out_ucast_pkts

    if interval >= 60:
        for i in range(duration/interval):
            graph_val = str(((i + 1) * interval / 60.0))
            graph_x_labels.append(graph_val + "m")
    else:
        for i in range(duration/interval):
            graph_val = str(((i + 1) * interval))
            graph_x_labels.append(graph_val + "s")

    print if_in_ucast_pkts
    print if_out_ucast_pkts
    print graph_x_labels
    return(if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels)


def generate_graph(if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels):
    '''
    Takes 3 lists as an input (if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels) and generates line graph in SVG format
    via pygal.
    '''
    in_out_pkts = pygal.Line()
    in_out_pkts.title = "Input / Output Unicast Packets - Fa4"
    in_out_pkts.add("InBytes", if_in_ucast_pkts)
    in_out_pkts.add("OutBytes", if_out_ucast_pkts)
    in_out_pkts.x_labels = graph_x_labels
    in_out_pkts.render_to_file("if_ucast_pkts.svg")



def  main():
    if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels = if_ucast_pkts(15, 300)
    generate_graph(if_in_ucast_pkts, if_out_ucast_pkts, graph_x_labels)
    print "Done..."







if __name__ == "__main__":
    main()
