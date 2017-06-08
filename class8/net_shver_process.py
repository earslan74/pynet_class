#!/usr/bin/env python

from net_system.models import NetworkDevice, Credentials 
import django
from netmiko import ConnectHandler
from datetime import datetime
from multiprocessing import Process, current_process

def show_version(a_device):
    creds = a_device.credentials
    print "#" * 30, a_device, "#" * 30
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address, username=creds.username, password=creds.password, port=a_device.port, secret="")
    print remote_conn.send_command("show version")
    


def main():
    django.setup()
    start_time = datetime.now()
    devices = NetworkDevice.objects.all()
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=show_version, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        print a_proc
        a_proc.join()    

    print "\nElapsed time: " + str(datetime.now() - start_time)

if __name__ == "__main__":
    main()
