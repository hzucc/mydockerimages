import pickle
import socket
import time

import cv2
import numpy
BUF_FLGSH = 'endendend'.encode()

def templatematch(img:numpy, template:numpy):
    # 加载图像和模板并转换为CUDA格式
    cuda_img = cv2.cuda_GpuMat()
    cuda_template = cv2.cuda_GpuMat()
    cuda_img.upload(img)
    cuda_template.upload(template)

    # 使用CUDA加速的模板匹配
    match = cv2.cuda.createTemplateMatching(cuda_img.type(), cv2.TM_SQDIFF_NORMED)
    result = match.match(cuda_img, cuda_template)

    # 将CUDA格式转换为OpenCV格式
    result = result.download()

    # 找到最佳匹配位置
    #(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    return result

if __name__ == "__main__":
    cv2.cuda.setDevice(0)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    server_address = ('0.0.0.0', 7779)
    server_socket.bind(server_address)
    # 监听连接
    server_socket.listen(1)

    print("端口7779")
    # 创建套接字
    while True:
        client_socket = None
        try:
            # 接受连接
            client_socket, client_address = server_socket.accept()
            # print("接收到来自", client_address, "的连接")

            # 接收数据
            response = b""
            buffer_size = 1024

            while True:
                data = client_socket.recv(buffer_size)
                if not data:
                    break
                response += data
                if response.endswith(BUF_FLGSH):
                    response = response[: len(response) - len(BUF_FLGSH)]
                    break
            req = pickle.loads(response)

            res = templatematch(req['img'], req['template'])
            # 找到最佳匹配位置
            res = cv2.minMaxLoc(res)

            # 发送结果给发送端
            req = pickle.dumps(res)
            # 发送数据
            total_sent = 0
            chunk = 1024
            while total_sent < len(req):
                # 发送数据到套接字的发送缓冲区
                sent = client_socket.send(req[total_sent: total_sent + chunk])
                if sent == 0:
                    # 发送缓冲区已满，无法发送数据
                    raise RuntimeError("Socket connection broken")
                total_sent += sent
            client_socket.send(BUF_FLGSH)
        except Exception as e:
            print(e)
        finally:
            # 关闭套接字连接
            if client_socket:
                client_socket.close()
        time.sleep(0.1)
