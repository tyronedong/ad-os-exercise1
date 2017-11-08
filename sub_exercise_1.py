import socket
import sys

# host = 'www.google.com'
# port = 80
#
# try:
#     remote_ip = socket.gethostbyname(host)
#
# except socket.gaierror:
#     # could not resolve
#     print('Hostname could not be resolved. Exiting')
#     sys.exit()
#
# print('Ip address of ' + host + ' is ' + remote_ip)


def server():
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 5678  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    s.listen(10)
    print('Socket now listening on port: ' + str(PORT))

    # now keep talking with the client
    while True:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data:
            break

        conn.sendall(reply)

    conn.close()
    s.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('method not specified(server or client)')
        exit()
    server()
    print('')
    pass