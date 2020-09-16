FROM python:3.6

MAINTAINER yongzhang24 <yongzhang24@iflytek.com>

RUN mkdir -p /template/logs
ADD app /template/app
ADD instance /template/instance
ADD base /template/base
ENV PATH $PATH:/template

WORKDIR /template
RUN pip install -r /base/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8080

CMD ["supervisord","-c","/template/base/supervisord.conf"]