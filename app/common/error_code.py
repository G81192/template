# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from enum import Enum

from app import app


class ErrorCode(Enum):
    SUCCESS = {'code': 0, 'message': u"成功"}
    SUCCESS_C = {'code': 0, 'message': u"创建成功"}
    SUCCESS_R = {'code': 0, 'message': u"查询成功"}
    SUCCESS_U = {'code': 0, 'message': u"修改成功"}
    SUCCESS_D = {'code': 0, 'message': u"删除成功"}

    INVALID_ARGS = {'code': app.config['ERROR_CODE_GENERAL_START'] + 1, 'message': u"参数不正确"}
    RESOURCE_EXISTED = {'code': app.config['ERROR_CODE_GENERAL_START'] + 2, 'message': u"资源已存在"}
