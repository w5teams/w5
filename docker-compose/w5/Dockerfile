FROM python:3.8.2
MAINTAINER jackzhou<jackzhou2016@qq.com>

RUN git clone https://github.com/w5teams/w5 \
    && cd w5 \
    && pip install -r requirements.txt -i https://pypi.douban.com/simple

WORKDIR /w5
EXPOSE 8888
CMD ["/usr/local/bin/python", "run.py"]
