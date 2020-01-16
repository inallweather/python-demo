import os
import socket
import sys

ADDR = ('172.40.91.224', 8888)


def do_login(client):
    while True:
        name = input('Enter you nickname')
        if not name:
            continue
        client.sendto(f'LOGIN {name}'.encode(), ADDR)
        data, addr = client.recvfrom(4096)
        if data.decode() == 'OK':
            print('你已经进入聊天室')
            return name
        else:
            print(data.decode() + '\n消息：', end='')


def do_send(client, name):
    while True:
        try:
            text = input('Enter the message:')
        except KeyboardInterrupt:
            text = 'quit'
        if not text:
            continue
        if text == 'quit':
            client.sendto(f'QUIT {name}', ADDR)
            sys.exit('退出聊天室')
        client.sendto(f'CHAT {name} {text}', ADDR)


def do_receive(client):
    while True:
        data, addr = client.recvfrom(4096)
        if data.decode() == 'QUIT':
            sys.exit()
        print(data.decode())


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    name = do_login(client)
    if name:
        pid = os.fork()
        if pid == 0:
            do_send(client, name)
        else:
            do_receive(client)


if __name__ == '__main__':
    main()
