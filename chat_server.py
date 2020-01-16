import os
import socket

ADDR = ('localhost', 4000)

user = {}


def do_login(server, name, addr):
    if name in user or '管理' in name:
        server.sendto('用户已经存在'.encode(), addr)
        return
    else:
        server.sendto('OK'.encode(), addr)
        msg = f'欢迎{name}加入群聊'
        for key, val in user.items():
            server.sendto(msg, val)
        user[name] = addr


def do_chat(server, name, content):
    msg = f'{name}:{content}'
    for key, val in user:
        if key != name:
            server.sendto(msg.encode(), val)


def do_exit(server, name):
    for key, addr in user:
        if key != name:
            server.sendto(f'{name}离开了聊天室', addr)
        else:
            server.sendto('QUIT'.encode(), addr)
    del user[name]


def request(server):
    while True:
        c, addr = server.recvfrom(4096)
        temp = c.decode().split(' ', 2)
        if temp[0] == 'LOGIN':
            do_login(server, temp[1], addr)
        elif temp[0] == 'CHAT':
            do_chat(server, temp[1], temp[2])
        elif temp[0] == 'QUIT':
            if temp[1] in user:
                do_exit(server, temp[1])


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    pid = os.fork()
    if pid == 0:
        msg = input('Enter message:')
        msg = f'CHAT 管理员 {msg}'
        server.sendto(msg.encode(), ADDR)
    else:
        request(server)


if __name__ == '__main__':
    main()
