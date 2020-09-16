# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from flask import Blueprint
from app import root_logger

exception = Blueprint('exception', __name__)


@exception.app_errorhandler(404)
def error_404(error):
    """
    raise 404 error
    :param error:
    :return:
    """
    return "Not Found", 404


@exception.app_errorhandler(405)
def error_405(error):
    """
    raise method error
    :param error:
    :return:
    """
    return "METHOD NOT ALLOWED", 405


@exception.app_errorhandler(Exception)
def error_500(error):
    """
    raise system error
    :param error:
    :return:
    """
    root_logger.exception(Exception)
    return 'INTERNAL SERVER ERROR', 500


class MyError(Exception):
    """
    """
    pass