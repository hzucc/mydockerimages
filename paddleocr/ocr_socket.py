import logging
import os
import pickle
import socket
import time
BUF_FLGSH = 'endendend'.encode()
from paddleocr import PaddleOCR

logging.basicConfig(level=logging.INFO)

dir_path = os.path.dirname(os.path.realpath(__file__))

def domain():
    PORT = 7777
    IP = '0.0.0.0'
    ocr = PaddleOCR(use_gpu=True)
    logging.info('加载ocr完毕')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP, PORT)
    server_socket.bind(server_address)
    server_socket.listen(1)
    # 创建套接字
    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(client_address)
        try:
            logging.info('循环')
            # 接收数据
            response = b""
            buffer_size = 1024
            while True:
                data = client_socket.recv(buffer_size)
                response += data
                if response.endswith(BUF_FLGSH):
                    response = response[: len(response) - len(BUF_FLGSH)]
                    break
            logging.info('接收结束')
            img = pickle.loads(response)
            logging.info('开始ocr...')
            res = ocr.ocr(img, cls=True)
            logging.info('结束ocr....')
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
            logging.info('发送结束')
        except Exception as e:
            logging.info(e)
        finally:
            # 关闭套接字连接
            if client_socket:
                client_socket.close()
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        domain()
    except Exception as e:
        logging.info(e)
    finally:
        logging.info('程序结束')
