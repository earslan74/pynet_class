#!/usr/bin/env python
import paramiko
from getpass import getpass
import time


remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class DeviceConnect(object):    
    def __init__(self, ip, uname, passwd):
        self.ip = ip
        self.uname = uname
        self.passwd = passwd
        self.config_mode = False
    
        remote_conn_pre.connect(self.ip, username=self.uname, password=self.passwd, look_for_keys=False, allow_agent=False)
        self.remote_conn = remote_conn_pre.invoke_shell()
        self.remote_conn.settimeout(6.0)

    def disable_paging(self):                
        self.remote_conn.send("terminal length 0\n")
        time.sleep(1)

    def send_cmd(self, cmd="\n"):    
        self.remote_conn.send(cmd+"\n")
        time.sleep(1)
        output = self.remote_conn.recv(5000)
        return output

    def conf_mode(self):    
        output = self.send_cmd("conf t")
        output = self.send_cmd()
        if output.strip().endswith("(config)#"):
            self.config_mode = True
        else:
            self.config_mode = False

    def exit_conf_mode(self):
        output = self.send_cmd("end")
        output = self.send_cmd()
        if output.strip().endswith("(config)#"):
            self.config_mode = True
        else:
            self.config_mode = False

    def disconnect(self):
        self.remote_conn.close()
        remote_conn_pre.close()


def print_output(output):
    out_list = output.split("\n")
    for line in out_list[1:-1]:
        print line    

def main():
    password = getpass()
    rtr2 = {"ip": "184.105.247.71", "username": "pyclass", "password": password}
    while True:
        buff_size = raw_input("Enter the log buffer size (4096 - 65000): ")
        if int(buff_size) >= 4096 and int(buff_size) <= 65000:
            break
        else:
            print "Buffer size is not valid! Should be in range 4096 - 65000.\n"
            continue
    rtr2_conn = DeviceConnect(rtr2["ip"], rtr2["username"], rtr2["password"])
    rtr2_conn.conf_mode()
    # print rtr2_conn.config_mode
    rtr2_conn.send_cmd("logging buffered " + buff_size)
    rtr2_conn.exit_conf_mode()
    # print rtr2_conn.config_mode
    output = rtr2_conn.send_cmd("show run | inc logging buffered")
    print_output(output)
    rtr2_conn.disconnect()
    

if __name__ == "__main__":
    main() 

