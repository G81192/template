# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from __future__ import absolute_import, unicode_literals

from celery.bin import beat
from app import celery

if __name__ == '__main__':
    beat = beat.beat(app=celery)
    options = {
        'loglevel': 'INFO',
        'scheduler_cls': 'app.services.framework.scheduler.DatabaseScheduler'
    }
    beat.run(**options)
