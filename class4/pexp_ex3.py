#!/usr/bin/env python

import pexpect
from getpass import getpass


class DeviceConnect(object):
    def __init__(self, ip, uname, passwd, timeout=3, port=22):
        self.ip = ip
        self.uname = uname
        self.passwd = passwd
        self.timeout = timeout
        self.port = port
        self.prompt = ""
        self.ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(self.uname, self.ip, self.port))

    def login(self):
        self.ssh_conn.expect('ssword:') 
        self.ssh_conn.sendline(self.passwd)
        self.ssh_conn.expect('#')
        router_name = self.ssh_conn.before 
        router_name = router_name.strip()
        prompt = router_name + self.ssh_conn.after 
        self.prompt = prompt.strip()
        return self.prompt

    def send_cmd(self, cmd="\n"):
        pretty_output = ""
        self.ssh_conn.sendline(cmd)
        self.ssh_conn.expect(self.prompt)        
        output = self.ssh_conn.before
        out_list = output.strip().split("\n")
        for line in out_list[1:]:
            pretty_output += line + "\n"
        return pretty_output

    def disable_paging(self, cmd="terminal length 0"):
        self.send_cmd()
        self.send_cmd(cmd)
        self.ssh_conn.expect(self.prompt)

def main(): 
    password = getpass()
    rtr2 = {"ip": "184.105.247.71", "username": "pyclass", "password": password}

    rtr2_conn = DeviceConnect(rtr2["ip"], rtr2["username"], rtr2["password"])
    rtr2_conn.login()
    rtr2_conn.disable_paging()
    output = rtr2_conn.send_cmd("show ip int brief")
    print output

    
    
    #pattern = re.compile(r'^Lic.*DI:.*$', re.MULTILINE)
    #ssh_conn.sendline('show version')
    #ssh_conn.expect(pattern)
    #print ssh_conn.after

    #pattern = re.compile(r'.*uptime is.*$', re.MULTILINE)
    #ssh_conn.sendline('show version')
    #ssh_conn.expect(pattern)
    #print ssh_conn.after

if __name__ == "__main__":
    main()
