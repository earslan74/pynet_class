#!/usr/bin/env python

from net_system.models import NetworkDevice, Credentials 
import django
from netmiko import ConnectHandler
from datetime import datetime
import threading


def show_version(a_device):
    creds = a_device.credentials
    print "#" * 30, a_device, "#" * 30
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address, username=creds.username, password=creds.password, port=a_device.port, secret="")
    print remote_conn.send_command("show version")
    


def main():
    django.setup()
    start_time = datetime.now()
    devices = NetworkDevice.objects.all()
    
    for a_device in devices:
        my_thread = threading.Thread(target=show_version, args=(a_device,))
        my_thread.start()

    main_thread = threading.currentThread()

    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            print some_thread
            some_thread.join()    

    print "\nElapsed time: " + str(datetime.now() - start_time)

if __name__ == "__main__":
    main()
