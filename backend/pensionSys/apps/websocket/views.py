from django.shortcuts import render
from  dwebsocket.decorators import accept_websocket
import socket
import time

class ssocket_9000():
    s = None
    @classmethod
    def get_socket(cls):
        if cls.s is None:
            cls.s = socket.socket()  # 创建 socket 对象
            port = 9000
            host = socket.gethostname()  # 获取本地主机名
            addr = (host, port)  # 设置地址tuple
            cls.s.bind(addr)  # 绑定端口
            cls.s.listen(100)  # 等待客户端连接
        return cls.s

class ssocket_9001():
    s = None
    @classmethod
    def get_socket(cls):
        if cls.s is None:
            cls.s = socket.socket()  # 创建 socket 对象
            port = 9001
            host = socket.gethostname()  # 获取本地主机名
            addr = (host, port)  # 设置地址tuple
            cls.s.bind(addr)  # 绑定端口
            cls.s.listen(100)  # 等待客户端连接
        return cls.s

@accept_websocket
def msg(request):
    if request.is_websocket():
        while 1:

            c, addr = ssocket_9000.get_socket().accept()  # 接收客户端的连接
            print('msg连接地址：', addr)
            msg = c.recv(1024).decode('utf-8')
            c.close()

            request.websocket.send(msg.encode())  # 发送给前段的数据
            time.sleep(0.1)

@accept_websocket
def data(request):
    if request.is_websocket():
        # request.websocket.send('1')
        while 1:

            c, addr = ssocket_9001.get_socket().accept()  # 接收客户端的连接
            print('data连接地址：', addr)
            msg = c.recv(1024).decode('utf-8')
            c.close()
            request.websocket.send(msg.encode())  # 发送给前段的数据
            time.sleep(0.1)