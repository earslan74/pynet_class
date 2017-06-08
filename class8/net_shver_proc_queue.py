#!/usr/bin/env python

from net_system.models import NetworkDevice, Credentials 
import django
from netmiko import ConnectHandler
from datetime import datetime
from multiprocessing import Process, current_process, Queue

def show_version_queue(a_device, q):
    output_dict = {}
    creds = a_device.credentials
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address, username=creds.username, password=creds.password, port=a_device.port, secret="")
    output = ("#" * 30) + str(a_device.device_name) + ("#" * 30) + "\n"
    output += remote_conn.send_command("show version") + "\n" 
    output += ("#" * 80) + "\n"
    output_dict[a_device.device_name] = output
    q.put(output_dict)

def main():
    django.setup()
    start_time = datetime.now()
    q = Queue(maxsize=20)
    devices = NetworkDevice.objects.all()
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=show_version_queue, args=(a_device,q))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
       # print a_proc
        a_proc.join()    

    while not q.empty():
        my_dict = q.get()
        for k,v in my_dict.iteritems():
            #print k
            print v

    print "\nElapsed time: " + str(datetime.now() - start_time)

if __name__ == "__main__":
    main()
