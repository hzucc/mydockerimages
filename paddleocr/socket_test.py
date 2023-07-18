import pickle
import socket

import cv2
import numpy as np

# 客户端套接字的地址和端口
server_address = ('192.168.1.2', 7777)


# 创建套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

BUF_FLGSH = 'endendend'.encode()

try:

    # 建立连接
    client_socket.connect(server_address)
    # 图片尺寸和背景颜色
    width = 800
    height = 500
    background_color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))

    # 生成随机数组
    random_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

    # 设置背景颜色
    random_array[:] = background_color

    # 将随机数组转换为图像
    image = cv2.cvtColor(random_array, cv2.COLOR_BGR2RGB)

    req = pickle.dumps(image)
    # 发送数据
    chunk = 1024
    total_sent = 0
    while total_sent < len(req):
        # 发送数据到套接字的发送缓冲区
        sent = client_socket.send(req[total_sent: total_sent + chunk])
        if sent == 0:
            # 发送缓冲区已满，无法发送数据
            raise RuntimeError("Socket connection broken")
        else:
            print('发送了' + str(sent) + '个字节')
        total_sent += sent
    client_socket.send(BUF_FLGSH)
    print('发送完毕')

    # 接收响应
    resp = b""
    buffer_size = 1024
    while True:
        data = client_socket.recv(buffer_size)
        if data:
            print('接收' + str(len(data)) + '个字节')
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


