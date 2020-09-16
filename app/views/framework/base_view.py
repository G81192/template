# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : template
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

from flask_restplus import Resource, reqparse
from app.common.error_code import ErrorCode
from flask import Blueprint, request, jsonify
from app import app
from app import api as swagger_api

baseProfile = Blueprint('baseProfile', __name__)


@app.route('/health', methods=['GET'])
def health():
    return "ok", 200


ns_project = swagger_api.namespace("base", description=u'base')


@ns_project.route('/test')
class TemplateTest(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('params', help=u"params")

    get_response = swagger_api.model('get task-runonce detail', {})

    @swagger_api.response(ErrorCode.SUCCESS_R.value.get('code'), ErrorCode.SUCCESS_R.value.get('message'),
                          model=get_response)
    @swagger_api.response(ErrorCode.INVALID_ARGS.value.get('code'), ErrorCode.INVALID_ARGS.value.get('message'))
    @swagger_api.expect(get_parser, validate=True)
    def get(self):
        params = request.values.get("params")
        ret = {"data": params}
        return jsonify(ret)
