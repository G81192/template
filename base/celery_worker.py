# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from __future__ import absolute_import, unicode_literals

from celery.bin import worker
from app import celery

if __name__ == '__main__':
    worker = worker.worker(app=celery)
    options = {
        'loglevel': 'INFO'
    }
    worker.run(**options)
