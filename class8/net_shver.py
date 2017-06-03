#!/usr/bin/env python

from net_system.models import NetworkDevice, Credentials 
import django
from netmiko import ConnectHandler
from datetime import datetime




def main():
    django.setup()
    start_time = datetime.now()
    devices = NetworkDevice.objects.all()
    for a_device in devices:
        creds = a_device.credentials
        print "#" * 30, a_device, "#" * 30
        remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address, username=creds.username, password=creds.password, port=a_device.port, secret="")
        print remote_conn.send_command("show version")

    print "\nElapsed time: " + str(datetime.now() - start_time)

if __name__ == "__main__":
    main()
