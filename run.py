# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from app import app

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run('0.0.0.0', port=6001, debug=True, threaded=True)
