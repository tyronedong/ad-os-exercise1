import socket
import sys
import os

End=bytes('EOF', encoding='utf-8')

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

    FBASE='filebase_server'

    # now keep talking with the client
    while True:
        # wait to accept command
        cmd = conn.recv(4096)

        if not cmd:
            print('Disconnected with ' + addr[0] + ':' + str(addr[1]))
            break

        cmd_recv = str(cmd, encoding='utf-8').strip()

        if cmd_recv == 'upload':
            filename_b = read_till_End(conn)
            conn.sendall(End)

            data_b = read_till_End(conn)

            try:
                with open('%s/%s'%(FBASE, str(filename_b, encoding='utf-8')), 'wb') as f:
                    f.write(data_b)
                message = 'upload success'
            except Exception as err:
                message = 'upload failed'

            print(message)
            conn.sendall(bytes(message, encoding='utf-8'))

        elif cmd_recv == 'download':
            filename_b = read_till_End(conn)
            filename = '%s/%s' % (FBASE, str(filename_b, encoding='utf-8'))
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    conn.sendfile(f)
                    conn.sendall(End)
                print('download success')
            else:
                conn.sendall(End)
                print('download failed')

        elif cmd_recv == 'list':
            files = os.listdir(FBASE)
            file_info = '\n'.join(files)
            conn.sendall(bytes(file_info, encoding='utf-8'))
            conn.sendall(End)
            print(file_info)
        else:
            reply = 'command not defined: ' + cmd_recv
            conn.sendall(bytes(reply, encoding='utf-8'))
            print(reply)

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
            print('\n请选择要进行的操作：\n'
                  'upload     upload a file to server file base\n'
                  'download   download a file from server file base\n'
                  'list       list all files available on server\n')
            cmd = sys.stdin.readline().strip('\n')

            s.sendall(bytes(cmd, encoding='utf-8'))

            if cmd == 'exit':
                break
            elif cmd == 'upload':
                print('please specify file path:')
                filepath = sys.stdin.readline().strip('\n')
                if not os.path.exists(filepath):
                    print('file "%s" not exists' % filepath)
                    continue

                send_append_End(s, bytes(os.path.basename(filepath), encoding='utf-8'))
                s.recv(1024)    # 用于阻塞进程
                with open(filepath, 'rb') as f:
                    s.sendfile(f)
                    s.sendall(End)
                res = s.recv(4096)
                print(str(res, encoding='utf-8'))
            elif cmd == 'download':
                print('please specify file name:')
                filename = sys.stdin.readline().strip('\n')
                send_append_End(s, bytes(filename, encoding='utf-8'))
                data_b = read_till_End(s)
                if len(data_b) == 0:
                    print('file "%s" not exists' % filename)
                else:
                    with open('filebase_client/%s' % filename, 'wb') as f:
                        f.write(data_b)
                    print('download success')

            elif cmd == 'list':
                data_b = read_till_End(s)
                file_info = str(data_b, encoding='utf-8')
                print(file_info)

            else:
                da = s.recv(4096)
                print(str(da, encoding='utf-8'))

        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

    s.close()

def send_append_End(s, data_b):
    s.sendall(data_b)
    s.sendall(End)

def read_till_End(s):
    total_data = []
    while True:
        data = s.recv(8192)
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            # check if end_of_data was split
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break

    return b''.join(total_data)

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