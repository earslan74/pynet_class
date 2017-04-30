#!/u sr/bin/env python

import pexpect
from getpass import getpass
import sys
import re


def main():
    ip_addr = "184.105.247.70"
    uname = "pyclass"
    passwd = getpass()
    port = 22

    ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(uname, ip_addr, port))
    # ssh_conn.logfile = sys.stdout # You may send the log to stdout or store it in a file
    ssh_conn.timeout = 3 
    ssh_conn.expect('ssword:') # After the ssh conn is established, look for 'ssword:' in the output
    ssh_conn.sendline(passwd) # Send the password -sendline inserts a newline at the end of the command itself, so no need to provide \n at the end of the command
    ssh_conn.expect('#')
    # print ssh_conn.before # Read all the output before the last expect, which is # (all output excluding # is printed)
    
    router_name = ssh_conn.before # Read the output before # and assign to router_name (but this one will include some spaces before the router name)
    router_name = router_name.strip() # So, you need to strip the spaces in order to get just the router name
    # print router_name
    # print ssh_conn.after # This will just bring the # sign
    prompt = router_name + ssh_conn.after 
    prompt = prompt.strip()
    # print prompt

    ssh_conn.sendline('show ip int brief')
    ssh_conn.expect(prompt) # Between this expect and the previous expect, the output is saved in the before attribute
    print ssh_conn.before  # So, you print the output between the previous 2 expects

    ssh_conn.sendline('terminal length 0')
    ssh_conn.expect(prompt)
    
    ssh_conn.sendline('show version')
    ssh_conn.expect(prompt)
    print ssh_conn.before
    
    pattern = re.compile(r'^Lic.*DI:.*$', re.MULTILINE)
    ssh_conn.sendline('show version')
    ssh_conn.expect(pattern)
    print ssh_conn.after

    pattern = re.compile(r'.*uptime is.*$', re.MULTILINE)
    ssh_conn.sendline('show version')
    ssh_conn.expect(pattern)
    print ssh_conn.after

if __name__ == "__main__":
    main()
