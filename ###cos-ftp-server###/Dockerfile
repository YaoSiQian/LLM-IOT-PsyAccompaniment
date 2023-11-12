# 使用 Python 2.7.18 作为基础镜像
FROM python:2.7.18

# 安装系统包和依赖库
RUN apt-get update && \
    apt-get install -y python-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install cos-python-sdk-v5>=1.6.5 pyftpdlib>=1.5.2 psutil>=5.6.1 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 克隆仓库并设置工作目录
RUN git clone https://github.com/tencentyun/cos-ftp-server-V5.git /app

# 设置工作目录
WORKDIR /app

# 运行安装
RUN mkdir /ftp && python setup.py install

# 开放端口范围 [60000, 60001]
EXPOSE 21
EXPOSE 60000
EXPOSE 60001

# 运行FTP Server
CMD ["python", "ftp_server.py"]

