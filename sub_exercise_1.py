import socket
import sys

host = 'www.google.com'
port = 80

try:
    remote_ip = socket.gethostbyname(host)

except socket.gaierror:
    # could not resolve
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('Ip address of ' + host + ' is ' + remote_ip)

if __name__ == '__main__':
    # if len(sys.argv) == 1:
    # print(sys.argv[1])
    pass