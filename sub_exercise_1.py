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

def client():
    host = 'localhost'
    port = 8888

    try:
        # create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    remote_ip = socket.gethostbyname(host)
    print(remote_ip)
    print(port)
    s.connect((remote_ip, port))
    print('Socket Connected to ' + host + ' on ip ' + remote_ip)

    while True:
        try:
            print('请投骰子(输入"go")')
            cmd = sys.stdin.readline()
            if cmd == 'exit':
                break

            # Set the whole string
            s.sendall(bytes(cmd, encoding='utf-8'))
            print('Message send successfully')

            # Now receive data
            reply = s.recv(4096)

            print(str(reply, encoding='utf-8'))

        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

    s.close()

def server():
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 8888  # Arbitrary non-privileged port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    try:
        s.bind((HOST, PORT))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    s.listen(10)
    print('Socket now listening on port: ' + str(PORT))

    # now keep talking with the client
    while True:
        # wait to accept a connection - blocking call
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        data = conn.recv(4096)
        #cmd_rece
        reply = 'OK...' + str(data, encoding='utf-8')
        if not data:
            break

        conn.sendall(bytes(reply, encoding='utf-8'))
        print(reply)

    conn.close()
    s.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('method not specified(server or client)')
        exit()
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client':
        client()
    print('finish')