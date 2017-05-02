#!/usr/bin/env python
import pexpect
from getpass import getpass
import sys


class DeviceConnect(object):
    def __init__(self, ip, uname, passwd, timeout=3, port=22):
        self.ip = ip
        self.uname = uname
        self.passwd = passwd
        self.timeout = timeout
        self.port = port
        self.prompt = ""
        self.config_mode = False
        self.ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(self.uname, self.ip, self.port))
        #self.ssh_conn.logfile = sys.stdout

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
        if self.config_mode == False:
            self.ssh_conn.expect(self.prompt)
        else:
            self.ssh_conn.expect('\(config\)#')
        output = self.ssh_conn.before
        out_list = output.strip().split("\n")
        for line in out_list[1:]:
            pretty_output += line + "\n"
        return pretty_output

    def disable_paging(self, cmd="terminal length 0"):
        self.send_cmd()
        self.send_cmd(cmd)

    def conf_mode(self, cmd="conf t"):
        self.send_cmd()
        self.config_mode = True
        self.send_cmd(cmd)
    
    def exit_conf_mode(self, cmd="end"):
        if self.config_mode == True:
            self.config_mode = False
            self.send_cmd(cmd)
        else:
            print "The device is not in config mode."
    
    def disconnect(self):
        self.ssh_conn.close()

def main(): 
    password = getpass()
    rtr2 = {"ip": "184.105.247.71", "username": "pyclass", "password": password}
    while True:
        buffer_size = raw_input("Enter the buffer size (4096 - 65000): ")
        if int(buffer_size) >= 4096 and int(buffer_size) <= 65000:
            break
        else:
            print "Invalid buffer size! Try again.."
            continue 
    rtr2_conn = DeviceConnect(rtr2["ip"], rtr2["username"], rtr2["password"])
    rtr2_conn.login()
    print "Logging in."
    rtr2_conn.disable_paging()
    print "Disabling paging."
    rtr2_conn.conf_mode()
    print "Entering config mode."
    if rtr2_conn.config_mode == True:
        print "Sending the command\n"
        rtr2_conn.send_cmd("logging buffered " + buffer_size)
    else:
        print "The device is not in config mode."
    rtr2_conn.exit_conf_mode()
    output = rtr2_conn.send_cmd("show run | inc logging buff")
    print output
    rtr2_conn.disconnect()
    
    
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
