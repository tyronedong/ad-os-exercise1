import socket
import sys
import random as rd

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

def stand_alone():
    while True:
        print('请输入算术表达式：')
        cmd = str(sys.stdin.readline()).strip('\n')
        if cmd == 'exit':
            break
        else:
            if not cmd.endswith('#'):
                cmd += '#'
            res = cal_expression(cmd)

        print('计算结果： ' + str(res))
        print('')

OPTR_PRI = [[1, 1, -1, -1, -1, 1, 1],
            [1, 1, -1, -1, -1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, -1, 1, 1],
            [-1, -1, -1, -1, -1, 0, 2],
            [-1, -1, -1, -1, 2, 1, 1],
            [-1, -1, -1, -1, -1, 2, 0]]
OPTR_DIC = {'+': 0, '-': 1, '*': 2, '/': 3, '(': 4, ')': 5, '#': 6}
OPTR_LIST = OPTR_DIC.keys()
NUM_LIST = ['0','1','2','3','4','5','6','7','8','9','.']

def cal_expression(expression):
    num_stack = []
    optr_stack = []
    optr_stack.append('#')

    if not check_legalcy(expression):
        print('illegal expression: ' + expression[:len(expression)-1])
        return None

    index = 0
    while True:
        if index >= len(expression):
            break
        chr = expression[index]

        if chr in NUM_LIST:
            val, l = read_float(expression, index)
            num_stack.append(val)
            index+=l
        elif chr in OPTR_LIST:
            top = optr_stack[len(optr_stack)-1]
            pri = OPTR_PRI[OPTR_DIC[top]][OPTR_DIC[chr]]
            if pri == 1:
                try:
                    top = optr_stack.pop()
                    num_2 = num_stack.pop()
                    num_1 = num_stack.pop()
                    num_stack.append(operate(num_1, top, num_2))
                except Exception as e:
                    print('illegal expression: ' + expression[:len(expression)-1])
                    break
            elif pri == -1:
                optr_stack.append(chr)
                index+=1
            elif pri == 0:
                optr_stack.pop()
                index+=1
            else:
                print('illegal expression: '+expression[:len(expression)-1])
                break
        else:
            print('illegal expression: '+expression[:len(expression)-1])
            break
    if len(optr_stack) == 0 and len(num_stack) == 1:
        return num_stack.pop()
    else:
        return None

def check_legalcy(expression):
    for s in expression:
        if not (s in OPTR_DIC or s in NUM_LIST):
            return False
    return True

def read_float(expression, start_index):
    tmp = ''
    for s in expression[start_index:]:
        if s in NUM_LIST:
           tmp+=s
        else:
            return float(tmp), len(tmp)
    return None

def operate(num_1, opt, num_2):
    if opt == '+':
        return num_1+num_2
    elif opt == '-':
        return num_1-num_2
    elif opt == '*':
        return num_1*num_2
    elif opt == '/':
        return num_1/num_2
    else:
        return None

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
            print('请输入算术表达式：')
            cmd = str(sys.stdin.readline()).strip('\n')
            if cmd == 'exit':
                break
            # Set the whole string
            s.sendall(bytes(cmd, encoding='utf-8'))
            reply = s.recv(4096)
            print('计算结果： ' + str(reply, encoding='utf-8'))
            print('')
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
        if not cmd_recv.endswith('#'):
            cmd_recv += '#'
        reply = str(cal_expression(cmd_recv))

        conn.sendall(bytes(reply, encoding='utf-8'))
        print('replt to client: ' + reply)

    conn.close()
    s.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('role not specified(server or client)')
        exit()
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client':
        client()
    else:
        stand_alone()
    # client()
    # server()
    # stand_alone()
    print('finish')