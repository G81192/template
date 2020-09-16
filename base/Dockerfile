FROM python:3.6

MAINTAINER yongzhang24 <yongzhang24@iflytek.com>

RUN mkdir -p /moss/logs
ADD app /moss/app
ADD instance /moss/instance
ADD base /moss/base
ENV PATH $PATH:/moss

WORKDIR /moss
RUN pip install -r /base/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8080

CMD ["supervisord","-c","/moss/supervisord.conf"]