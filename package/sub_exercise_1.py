import socket
import sys
import math
import random as rd
import re
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

OPTR_PRI = [[1, 1, -1, -1, -1, 1, -1, 1],
            [1, 1, -1, -1, -1, 1, -1, 1],
            [1, 1, 1, 1, -1, 1, -1, 1],
            [1, 1, 1, 1, -1, 1, -1, 1],
            [-1, -1, -1, -1, -1, 0, -1, 2],
            [-1, -1, -1, -1, 2, 1, -1, 1],
            [1, 1, 1, 1, -1, 1, 2, 1],
            [-1, -1, -1, -1, -1, 2, -1, 0]]
OPTR_DIC = {'+': 0, '-': 1, '*': 2, '/': 3, '(': 4, ')': 5, '^':6, '#': 7}
OPTR_LIST = OPTR_DIC.keys()
NUM_LIST = ['0','1','2','3','4','5','6','7','8','9','.']

def cal_expression(expression):
    if not expression.endswith('#'):
        expression += '#'
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
    elif opt == '^':
        return math.pow(num_1, num_2)
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
            print('请输入您的姓名：')
            name = str(sys.stdin.readline()).strip('\n')
            s.sendall(bytes(name, encoding='utf-8'))    # 发送名字

            print('请输入本次要做的题数：')
            while True:
                num = str(sys.stdin.readline()).strip('\n')
                if (not num.isdigit()) or int(num)<=0:
                    print('请输入正整数：')
                    continue
                else:
                    break
            # 把题数发给服务器
            s.sendall(bytes(num, encoding='utf-8'))     # 发送题数

            for i in range(int(num)):
                question = str(s.recv(1024),encoding='utf-8')     # 接受问题
                print('%s: %s'%(i+1,question))
                answer = str(sys.stdin.readline()).strip('\n')
                s.sendall(bytes(answer, encoding='utf-8'))        # 发送答案

            result = str(s.recv(1024), encoding='utf-8')    # 接受结果
            print(result)

        except socket.error:
            # Send failed
            print('Send failed')
            sys.exit()

is_float = re.compile('^-?\d+(\.\d*)?$')

def server():
    exam_result = {}

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

    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    while True:
        print(exam_result)

        name_b = conn.recv(1024)    # 接受名字
        name = str(name_b, encoding='utf-8')
        num_b = conn.recv(1024)     # 接受题数
        num = int(str(num_b,encoding='utf-8'))

        if exam_result.get(name):   # 记录考生信息
            exam_result[name].append([num, 0])
        else:
            exam_result[name] = [[num, 0]]

        for i in range(num):
            question = gen_question()
            print('question %s: %s'%(i+1, question))
            conn.sendall(bytes(question, encoding='utf-8'))     # 发送问题
            answer = str(conn.recv(1024), encoding='utf-8')     # 接受答案
            if not is_float.match(answer):
                print('illegal result from client: '+answer)
                continue
            if abs(cal_expression(question) - float(answer)) < 0.001:
                cur_exam = exam_result[name].pop()
                cur_exam[1] += 1
                exam_result[name].append(cur_exam)
                print('right answer from client: '+answer)
            else:
                print('wrong answer from client: '+answer)

        cur_exam = exam_result[name].pop()
        exam_result[name].append(cur_exam)
        result = 'correct: %s/%s\nfinal score: %s' % (cur_exam[1], cur_exam[0], cur_exam[1]/cur_exam[0])
        conn.sendall(bytes(result, encoding='utf-8'))   # 发送结果
        print('replt to client: ' + result)


def gen_question_bank(number):
    for i in range(number):
        pass

def gen_question_raw():
    num_count = rd.randint(3, 5)    # 生成num_count个值参与计算

    opr_candi = ['+','+','+','-','-','-','*','/','^']
    opr_add_minus = ['+','-']
    opr_higher = ['*','/','^']
    exp_list = []
    flag = True
    for i in range(num_count):

        # 生成左括号
        if flag and rd.random() < 0.25 and i < num_count-1:
            exp_list.append('(')
            flag = False

        # 生成数字，控制幂较小
        if len(exp_list) > 1 and exp_list[len(exp_list)-1] == '^':
            exp_list.append(str(rd.randint(2, 6)))
        elif len(exp_list) > 2 and (exp_list[len(exp_list)-1]=='(' and exp_list[len(exp_list)-2]=='^'):
            exp_list.append(str(rd.randint(1, 5)))
        elif len(exp_list) > 4 and (exp_list[len(exp_list)-3]=='(' and exp_list[len(exp_list)-4]=='^'):
            exp_list.append(str(rd.randint(1, 5)))

        else:
            exp_list.append(str(rd.randint(1,100)))

        # 生成右括号
        if len(exp_list) > 3 and exp_list[len(exp_list)-4] == '(':
            exp_list.append(')')
            flag = True

        # 生成运算符
        if not flag:    # 左括号生成，则括号里只有加减法
            exp_list.append(opr_add_minus[rd.randrange(0, len(opr_add_minus))])
        elif exp_list[len(exp_list)-1]==')':    # 上一个是右括号，则后面跟一个乘除幂运算
            exp_list.append(opr_higher[rd.randrange(0, len(opr_higher))])
        else:   # 都不是，则全局随机生成
            exp_list.append(opr_candi[rd.randrange(0, len(opr_candi))])
    exp_list.pop()  # 去掉最后一个多余的运算符

    expression = ''.join(exp_list)

    if cal_expression(expression):
        return expression
    else:
        return None

def gen_question():
    while True:
        expression = gen_question_raw()
        if expression:
            return expression

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
    # for i in range(45):
    #     print(gen_question())
    print('finish')
