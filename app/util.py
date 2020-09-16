# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

import json
import socket
import zipfile
import os
from flask import request
import redis
from redis.sentinel import Sentinel
import pytz
import re
import random
from celery import Celery, platforms
from app import app, api_logger


class Util(object):

    if app.config.get('REDIS_CLUSTER'):
        sentinel = Sentinel(app.config['REDIS_SENTINEL_LIST'], socket_timeout=5)
        redis = sentinel.master_for(app.config['REDIS_CLUSTER_NAME'], db=app.config['REDIS_DB'], socket_timeout=5)
    else:
        redis = redis.StrictRedis(app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'],
                                  password=app.config['REDIS_PASS'])

    def __init__(self):
        pass

    @staticmethod
    def make_celery(app):
        celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        TaskBase = celery.Task
        platforms.C_FORCE_ROOT = True  # 允许以root用户启动

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
        return celery

    @staticmethod
    def can_tune_to(v, t):
        try:
            t(v)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_ip_addr():
        ip1 = request.headers.get('X-Forwarded-For')
        ip2 = request.headers.get('X-Real-Ip')
        ip3 = request.remote_addr
        if ip1:
            return ip1.split(',')[0]
        elif ip2:
            return ip2.split(',')[0]
        else:
            return ip3

    @staticmethod
    def check_date_str(s):
        try:
            if re.match('\d\d\d\d-\d\d-\d\d', s):
                return s
        except:
            return None
        return None

    @staticmethod
    def utc2local(d):
        local_tz = pytz.timezone(app.config.get('TIMEZONE'))
        local_dt = d.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_tz.normalize(local_dt)

    @staticmethod
    def replace_bad_word(s):
        s = s.replace("%5C", "%5C%5C")
        s = s.replace("%26", "%5Cu0026")
        s = s.replace("%3D", "%5Cu003D")
        s = s.replace("%22", "%5C%22")
        s = s.replace("%25", "%5Cu002525")
        return s

    @staticmethod
    def generate_passwd():
        alphabeta = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'
        number = '0123456789'
        all = [alphabeta, number]
        length = random.randint(8, 10)
        ret = list()
        i = random.randint(0, len(all[0]) - 1)
        ret.append(all[0][i])
        for l in range(length):
            s = random.randint(0, 1)
            i = random.randint(0, len(all[s])-1)
            ret.append(all[s][i])
        return ''.join(ret)

    @staticmethod
    def jsbool2pybool(val):
        if val == 'true':
            return True
        elif val == 'false':
            return False

    @staticmethod
    def match_json(val):
        try:
            json.dumps(val)
            return True
        except:
            return False

    @staticmethod
    def unzip(ori_file_path, target_file_path):
        # zipfile解压
        z = zipfile.ZipFile(ori_file_path, 'r')
        z.extractall(path=target_file_path)
        z.close()

    @staticmethod
    def del_file(workspace):
        os.system("rm -rf {}".format(workspace))

    @staticmethod
    def get_host_ip():
        """
        查询本机ip地址
        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @staticmethod
    def log_request_api_info(path):
        """
        打印请求ip和路径
        :return:
        """
        ip = Util.get_ip_addr()
        api_logger.debug("api request with: ip:{}, path:{}".format(ip, path))