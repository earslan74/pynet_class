#!/usr/bin/env python
# Takes a list of cisco devices, queries each device for running config change via SNMPv3 and sends email
# the device name & running config change time of each device 
import snmp_helper
import email_helper
import time
import pickle

RUNN_LAST_CHANGED = "1.3.6.1.4.1.9.9.43.1.1.1.0"
RUNN_LAST_SAVED = "1.3.6.1.4.1.9.9.43.1.1.2.0" 
START_LAST_CHANGED = "1.3.6.1.4.1.9.9.43.1.1.3.0"
SYS_UP_TIME = "1.3.6.1.2.1.1.3.0"
SYS_NAME = "1.3.6.1.2.1.1.5.0"

dev_list = ["184.105.247.70", "184.105.247.71"]

a_user = "pysnmp"
auth_key = "galileo1"
encrypt_key = "galileo1"
snmp_user = (a_user, auth_key, encrypt_key)


def gen_conf_record(dev_list):
    '''
    Takes a list of Cisco device IP addresses, and queries each device's sysuptime, runn_conf_last_change,
    runn_conf_last_saved, and sysname via SNMPv3.
    
    Returns a dict of list of sys_name, runn_last_changed, runn_last_saved, current_time_in_secs as a a value 
    of each device.
    '''
    conf_record = {}
    for device in dev_list:
        snmp_data = snmp_helper.snmp_get_oid_v3((device, 161), snmp_user, oid=SYS_UP_TIME)
        sys_up = snmp_helper.snmp_extract(snmp_data)
        snmp_data = snmp_helper.snmp_get_oid_v3((device, 161), snmp_user, oid=RUNN_LAST_CHANGED)
        runn_last_changed = snmp_helper.snmp_extract(snmp_data)
        snmp_data = snmp_helper.snmp_get_oid_v3((device, 161), snmp_user, oid=RUNN_LAST_SAVED)
        runn_last_saved = snmp_helper.snmp_extract(snmp_data)
        snmp_data = snmp_helper.snmp_get_oid_v3((device, 161), snmp_user, oid=SYS_NAME)
        sys_name = snmp_helper.snmp_extract(snmp_data)
        conf_record[device] = [sys_name, sys_up, runn_last_changed, runn_last_saved, time.time()]
    return conf_record

def check_conf_change(dev_list, prev_conf_record, conf_record):
    '''
    Takes the list of device IP addresses, dict of previous config change record saved in pickle file, and
    the dict of the most recent conf change record, and compares the values to detect if a config change
    took place on the devices.

    Returns the dict of device_name: time_of_change key/value pairs.
    ''' 
    dev_change = {}
    for dev in dev_list:
        prev_run_change = float(prev_conf_record[dev][2])/100
        run_change = float(conf_record[dev][2])/100
        if run_change != prev_run_change:
            sys_up = float(conf_record[dev][1])/100
            time_diff = sys_up - run_change
            check_time = float(conf_record[dev][4])
            time_of_change = time.strftime("%d %b %Y %H:%M:%S", time.gmtime(check_time-time_diff))
            print dev, time_of_change
            dev_name = conf_record[dev][0]
            dev_change[dev_name] = time_of_change
    return dev_change   

def email_change(dev_change):
    '''
    Takes the dev_change dict, which includes device_name: time_of_change key/value pairs, and send email to the recipient
    of these device changes.
    '''
    recipient = "uk.earslan@gmail.com"
    subject = "Device Config Change"
    sender = "ktbyers@twb-tech.com"
    device_time = ""
    for i in dev_change:
        device_time += i + " on " + dev_change[i] + " GMT" + "\n"
    message = '''

Config changes took place on the device(s) listed below.

{0} 


Regards,

Erdem
'''.format(device_time)

    email_helper.send_mail(recipient, subject, message, sender)
    print message 

def main():

    with open("conf_records.pkl", "rb") as f:
        prev_conf_record = pickle.load(f)
    conf_record = gen_conf_record(dev_list)
    print conf_record
    dev_change = check_conf_change(dev_list, prev_conf_record, conf_record)
    print dev_change
    if dev_change:
        email_change(dev_change)
    
    with open("conf_records.pkl", "wb") as f:
        pickle.dump(conf_record, f)



if __name__ == "__main__":
    main()

