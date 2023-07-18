FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

#https://github.com/cudawarped/opencv-python-cuda-wheels/releases

ADD /dist/* /dist/

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip libxml2 wget && \
    cp /dist/libnvcuvid.so /usr/local/cuda-11.7/lib64 && \
    cp /dist/libnvidia-encode.so /usr/local/cuda-11.7/lib64 && \
    wget https://github.com/cudawarped/opencv-python-cuda-wheels/releases/download/4.6.0/opencv_contrib_python_rolling-4.6.0.20220918-cp36-abi3-linux_x86_64.whl && \
    pip install opencv_contrib_python_rolling-4.6.0.20220918-cp36-abi3-linux_x86_64.whl && \
    apt-get install -y ffmpeg && \
    ldconfig && \
    cp /dist/app.py /app.py && \
    rm -rf /dist

CMD ["python3", "/app.py"]

EXPOSE 7779


#docker run --name opencv-gpu -d -p 7779:7779 --gpus all --memory=200m --memory-swap=2g --restart=always hzucc/opencv-python-gpu:latest

