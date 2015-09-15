import telnetlib
import time
import sys
import os

def write_string(tn, string, endchar):
    for c in string:
        tn.write(c.encode('ascii'))
        time.sleep(0.2)
    tn.write(endchar.encode('ascii'))

pid = os.fork()

if pid != 0:
    sys.exit(0)


filename = sys.argv[1]
host = sys.argv[2]
user = 'admin'
password = 'admin'
ip = '10.0.0.5'

print('Connecting to host: {}'.format(host))
tn = telnetlib.Telnet(host)
#tn.write("vt100\r\n".encode('ascii'))



#tn.write(user.encode('ascii') + '\t'.encode('ascii'))
#tn.write(password.encode('ascii') + "\r\n".encode('ascii'))

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

