            print('请选择要进行的操作：\n'
                  'upload\tupload a file to server file base\n'
                  'download\tdownload a file from server file base'
                  'list\tlist all files available on server')
            cmd = str(sys.stdin.readline()).strip('\n')
            if cmd == 'exit':
                break

            # Set the whole string
            s.sendall(bytes(cmd, encoding='utf-8'))
            s.send()
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