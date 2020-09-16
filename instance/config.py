# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

LOG_DIR = 'E:\\project\\logs\\moss\\'

SQLALCHEMY_DATABASE_URI = ''
SQLALCHEMY_BINDS = {
    'main': SQLALCHEMY_DATABASE_URI
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

REDIS_CLUSTER = False
REDIS_SENTINEL_LIST = []
REDIS_CLUSTER_NAME = ''

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASS = ''

TIMEZONE = 'Asia/Shanghai'

if REDIS_CLUSTER:
    CELERY_BROKER_URL = ''
    BROKER_TRANSPORT_OPTIONS = {
        "master_name": REDIS_CLUSTER_NAME
    }
else:
    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

CELERY_RESULT_BACKEND = 'db+mysql://root:root@127.0.0.1:3306/moss'
CELERY_TASK_RESULT_EXPIRES = 0
CELERY_RESULT_DB_TABLENAMES = {
    'task': 'celery_taskmeta',
    'group': 'celery_tasksetmeta',
}
CELERY_TIMEZONE = TIMEZONE
CELERY_ACCEPT_CONTENT = ['pickle', 'json']

ERROR_CODE_GENERAL_START = 10000