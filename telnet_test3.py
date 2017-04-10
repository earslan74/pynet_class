#!/usr/bin/env python
import telnetlib
import time

TELNET_PORT = 23
TELNET_TIMEOUT = 6
cmd = "show ip int brief"

def send_cmd(remote_conn, cmd):
    '''
    Send command through the telnet connection.
    Telnet connection instance and the command to be sent to the device are given as the function input.
    Output from the command execution is returned.
    '''
    cmd = cmd.strip()
    output = remote_conn.write(cmd + "\n")
    time.sleep(1)
    output = remote_conn.read_very_eager()  # output is a string
    out_list = output.split("\r\n") # Output is transformed to a list
    pretty_output = "\r\n" + "\r\n".join(out_list[1:-2]) + "\r\n"
    #for i in out_list[1:-2]:
    #    pretty_output += i + "\r\n"

    return pretty_output

def login(remote_conn, username, password): 
    output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
    output = remote_conn.write(username + "\n")
    output = remote_conn.read_until("assword:", TELNET_TIMEOUT)
    output = remote_conn.write(password + "\n")
    time.sleep(1)
    output = remote_conn.read_very_eager()
    return output

def main():
    ip_addr = "184.105.247.70"
    username = "pyclass"
    password = "88newclass"

    remote_conn = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)

    output = login(remote_conn, username, password)
    output = send_cmd(remote_conn, "terminal length 0")
    output = send_cmd(remote_conn, "show ip interface brief")
    print output

    remote_conn.close()


if __name__ == "__main__":
    main()

