import socket
import sys

def server():
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 8888  # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print('Socket now listening on port: ' + str(PORT))

    # wait for client connect
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # now keep talking with the client
    while True:
        # wait to accept a connection - blocking call
        data = conn.recv(4096)

        if not data:
            print('Disconnected with ' + addr[0] + ':' + str(addr[1]))
            break

        cmd_recv = str(data, encoding='utf-8').strip()

        if cmd_recv == 'go':
            # reply = str(rd.randint(1, 6))
            pass
        else:
            reply = 'command not defined: ' + cmd_recv

        conn.sendall(bytes(reply, encoding='utf-8'))
        print('replt to client: ' + reply)

    conn.close()
    s.close()

def client():
    host = 'localhost'
    port = 8888

    # create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # establish connect
    remote_ip = socket.gethostbyname(host)
    s.connect((remote_ip, port))
    print('Socket Connected to ' + host + ' on ip ' + remote_ip + ' and port ' + str(port))

    while True:
        try:
            print('请选择要进行的操作：\n'
                  'upload\tupload a file to server file base\n'
                  'download\tdownload a file from server file base'
                  'list\tlist all files available on server')
            cmd = sys.stdin.readline().strip('\n')

            if cmd == 'exit':
                break
            elif cmd == 'upload':
                print('please specify file path:')
                filepath = sys.stdin.readline().strip('\n')
                with open(filepath, 'rb') as f:
                    s.sendfile(f)
            elif cmd == 'download':
                pass
            elif cmd == 'list':
                pass

            # Set the whole string
            s.sendall(bytes(cmd, encoding='utf-8'))
            # print('Message send successfully')

            # Now receive data
            reply = s.recv(4096)
            s.sendfile()
            print('骰子点数： ' + str(reply, encoding='utf-8').strip())
            print('')
        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

    s.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('role not specified(server or client)')
        exit()
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client':
        client()
    # client()
    # server()
    print('finish')