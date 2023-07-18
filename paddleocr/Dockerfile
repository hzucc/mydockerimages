FROM paddlecloud/paddleocr:2.5-gpu-cuda10.2-cudnn7-latest
#https://mnopgu9h.mirror.aliyuncs.com
ADD ocr_socket.py /

CMD ["python3", "/ocr_socket.py"]

EXPOSE 7777

#docker run --name paddleocr --gpus all -p 7777:7777 -d --restart=always --memory=400m --memory-swap=3g hzucc/paddleocr:latest