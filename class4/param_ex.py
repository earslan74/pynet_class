#!/usr/bin/env python
import paramiko
from getpass import getpass
import time


def disable_paging(remote_conn):
    remote_conn.send("terminal length 0\n")
    time.sleep(1)

def send_cmd(remote_conn, cmd='\n'):    
    remote_conn.send(cmd+"\n")
    time.sleep(1)
    output = remote_conn.recv(5000)
    return output

def print_output(output):
    out_list = output.split("\n")
    for line in out_list[1:-1]:
        print line    

def main():
    password = getpass()
    rtr2 = {"ip": "184.105.247.71", "username": "pyclass", "password": password}

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(rtr2["ip"], username=rtr2["username"], password=rtr2["password"], look_for_keys=False, allow_agent=False)
    remote_conn = remote_conn_pre.invoke_shell()
    remote_conn.settimeout(6.0)
    
    disable_paging(remote_conn)
    output = send_cmd(remote_conn)
    output = send_cmd(remote_conn, "show version")
    print_output(output)

if __name__ == "__main__":
    main() 

