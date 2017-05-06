#!/usr/bin/env python

import argparse
import telnetlib
import time
import sys
import os


def write_string(tn, string, endchar):
    for c in string:
        tn.write(c.encode('ascii'))
        time.sleep(0.2)
    tn.write(endchar.encode('ascii'))


def main():
    pid = os.fork()

    if pid != 0:
        sys.exit(0)

    parser = argparse.ArgumentParser(description='Connect via telnet and configure LGS326 switches')
    parser.add_argument('-c', '--config', dest='filename', action='store',
                        help='Config file for the switch', required=True)
    parser.add_argument('-s', '--switch', dest='host', action='store',
                        help='IP address of the switch', required=True)
    parser.add_argument('-t', '--tftp', dest='ip', action='store', help='IP address of the TFTP server', required=True)
    parser.add_argument('-u', '--username', dest='user', action='store', help='Username', required=False, default='admin')
    parser.add_argument('-p', '--passsword', dest='password', action='store', help='Password',
                        required=False, default='admin')

    args = parser.parse_args()

    filename = args.filename
    host = args.host
    user = args.user
    password = args.password
    ip = args.ip

    print('Connecting to host: {}'.format(host))
    tn = telnetlib.Telnet(host)

    print('Sending username: {}'.format(user))
    write_string(tn, user, '\t')
    print('Sending password: {}'.format(password))
    write_string(tn, password, '\r\n')
    write_string(tn, '1', '\r\n')
    write_string(tn, '5', '\r\n')
    write_string(tn, '1', '\r\n')
    write_string(tn, '', '\t')
    write_string(tn, '', '\r\n')
    time.sleep(1.5)
    write_string(tn, '    ', '\t')
    time.sleep(1.5)
    write_string(tn, '  ', '\t')
    time.sleep(3.5)
    print('Sending filename: {}'.format(filename))
    write_string(tn, filename, '\t')
    time.sleep(3.5)
    print('Sending ip')
    write_string(tn, ip, '\x1b')
    time.sleep(2)
    write_string(tn, '', '\t')
    write_string(tn, '', '\r\n')

    time.sleep(3)

if __name__ == '__main__':
    main()
