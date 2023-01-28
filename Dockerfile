FROM amd64/python:3.8.2
MAINTAINER SanJin<lauixData@gmail.com>
WORKDIR /w5
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY . .
CMD ["supervisord", "-c", "/etc/supervisord.conf"]