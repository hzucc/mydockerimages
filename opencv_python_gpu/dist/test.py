import pickle
import socket
import numpy as np
import cv2


# 客户端套接字的地址和端口
server_address = ('192.168.1.2', 7779)

# 创建套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUF_FLGSH = 'endendend'.encode()

try:

    # 建立连接
    client_socket.connect(server_address)
    template = np.zeros((100, 100), dtype=np.uint8)
    template[25:75, 25:75] = 255
    img = np.zeros((480, 640), dtype=np.uint8)
    img[200:300, 200:300] = 255


    data = {
        "img":img,
        "template":template
    }

    req = pickle.dumps(data)
    # 发送数据
    chunk = 1024
    total_sent = 0
    while total_sent < len(req):
        # 发送数据到套接字的发送缓冲区
        sent = client_socket.send(req[total_sent: total_sent + chunk])
        if sent == 0:
            # 发送缓冲区已满，无法发送数据
            raise RuntimeError("Socket connection broken")
        total_sent += sent
    client_socket.send(BUF_FLGSH)

    # 接收响应
    resp = b""
    buffer_size = 1024
    while True:
        data = client_socket.recv(buffer_size)
        if data:
            resp += data
            if resp.endswith(BUF_FLGSH):
                resp = resp[:len(resp) - len(BUF_FLGSH)]
                break
    res = pickle.loads(resp)
    print(res)
except Exception as e:
    print('异常')
    print(e)
finally:
    # 关闭连接
    client_socket.close()
    input("按下任意键后结束：")


