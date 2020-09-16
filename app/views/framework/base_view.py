# -*- coding: utf8 -*-

"""
@author: zhangyong
@project : moss
@file: te.py
@time: 2020/9/16 11:04
@desc:
"""

import json
from flask_restplus import fields, Resource, reqparse
from app.common.error_code import ErrorCode
from app.services.framework.scheduler_service import SchedulerService
from flask import Blueprint, request, jsonify
from app import app
from app.util import Util
from app import api as swagger_api

baseProfile = Blueprint('baseProfile', __name__)


@app.route('/health', methods=['GET'])
def health():
    return "ok", 200


ns_project = swagger_api.namespace("base", description=u'base')

perPage = 20


@ns_project.route('/api/task-runonce/runonce')
class TaskRunonce(Resource):
    post_parser = swagger_api.model('task-runonce', {
        'task': fields.String(required=True, description=u'任务名',
                              example="app.services.framework.task_pool.sync_department_and_user"),
        'args': fields.List(fields.String, description=u'args'),
        'kwargs': fields.Raw(description=u'kwargs')
    })

    @swagger_api.response(ErrorCode.SUCCESS.value.get('code'), ErrorCode.SUCCESS.value.get('message'))
    @swagger_api.response(ErrorCode.INVALID_ARGS.value.get('code'), ErrorCode.INVALID_ARGS.value.get('message'))
    @swagger_api.expect(post_parser, validate=True)
    def post(self):
        data = request.json
        task = data.get('task')
        args = json.dumps(data.get('args', []))
        kwargs = json.dumps(data.get('kwargs', {}))
        if not args:
            args = '[]'
        if not kwargs:
            kwargs = '{}'
        ret = dict()
        if task:
            if SchedulerService.run_task_once(task, args, kwargs):
                ret.update(ErrorCode.SUCCESS_C.value)
            else:
                ret.update(ErrorCode.CREATE_FAILED.value)
        else:
            ret.update(ErrorCode.CREATE_FAILED.value)
        return jsonify(ret)


@ns_project.route('/api/task-runonce/detail')
class TaskRunonceDetail(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('query', help=u"搜索字段/任务名")
    get_parser.add_argument('startAt', help=u"任务开始时间")
    get_parser.add_argument('p', help=u"页数")
    get_parser.add_argument('id', help=u"任务Id")

    get_response = swagger_api.model('get task-runonce detail', {})

    @swagger_api.response(ErrorCode.SUCCESS_R.value.get('code'), ErrorCode.SUCCESS_R.value.get('message'),
                          model=get_response)
    @swagger_api.response(ErrorCode.INVALID_ARGS.value.get('code'), ErrorCode.INVALID_ARGS.value.get('message'))
    @swagger_api.expect(get_parser, validate=True)
    def get(self):
        sh_id = request.values.get('id')
        if sh_id:
            if Util.can_tune_to(sh_id, int):
                td = SchedulerService.get_task_history_detail(int(sh_id))
                ret = dict()
                if td:
                    ret['result'] = 1
                    ret['data'] = td
                else:
                    ret['result'] = 2
                return jsonify(ret)
        else:
            query = request.values.get('query', '')
            start_at = Util.check_date_str(request.values.get('startAt'))
            page = request.values.get('p', 1)
            if Util.can_tune_to(page, int):
                pager = SchedulerService.get_task_history(query, start_at).paginate(int(page), perPage, False)
                ret = dict()
                ret['result'] = 1
                his_list = pager.items
                data = dict()
                data['hisList'] = [e.serialize() for e in his_list]
                data['prevNum'] = pager.prev_num
                data['nextNum'] = pager.next_num
                data['total'] = pager.total
                data['perPage'] = perPage
                ret['data'] = data
                return jsonify(ret)
        return "error", 400


@app.route('/task-runonce/runonce', methods=['POST'])
def task_runonce__runonce():
    task = request.values.get('task')
    args = request.values.get('args', '[]')
    kwargs = request.values.get('kwargs', '{}')
    if not args:
        args = '[]'
    if not kwargs:
        kwargs = '{}'
    if task:
        ret = dict()
        if SchedulerService.run_task_once(task, args, kwargs):
            ret['result'] = 1
            return jsonify(ret)
    return "error", 400


@app.route('/task-config/schedule', methods=['GET', 'PUT', 'DELETE', 'POST'])
def task_config__schedule():
    if request.method == 'GET':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            ret = dict()
            ret['result'] = 1
            ret['data'] = SchedulerService.get_schedule_detail(int(sid))
            return jsonify(ret)
        else:
            ret = dict()
            ret['result'] = 1
            ss = SchedulerService.get_schedule_list()
            ret['data'] = [e.serialize() for e in ss]
            return jsonify(ret)
    elif request.method == 'DELETE':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            ret = dict()
            ret['result'] = 1
            SchedulerService.del_schedule(int(sid))
            return jsonify(ret)
    elif request.method == 'PUT':
        name = request.values.get('name')
        task = request.values.get('task')
        args = request.values.get('args')
        kwargs = request.values.get('kwargs')
        enabled = request.values.get('enabled')
        every = request.values.get('every')
        period = request.values.get('period')
        minute = request.values.get('minute')
        hour = request.values.get('hour')
        day_of_week = request.values.get('day_of_week')
        day_of_month = request.values.get('day_of_month')
        month_of_year = request.values.get('month_of_year')
        enabled = enabled == 'true'
        if every and Util.can_tune_to(every, int):
            ret = dict()
            ret['result'] = 1
            SchedulerService.add_schedule(name, task, args, kwargs, enabled, every=every, period=period)
            return jsonify(ret)
        elif minute or hour or day_of_week or day_of_month or month_of_year:
            ret = dict()
            ret['result'] = 1
            SchedulerService.add_schedule(name, task, args, kwargs, enabled, minute=minute, hour=hour,
                                          day_of_week=day_of_week, day_of_month=day_of_month,
                                          month_of_year=month_of_year)
            return jsonify(ret)
    elif request.method == 'POST':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            name = request.values.get('name')
            task = request.values.get('task')
            args = request.values.get('args')
            kwargs = request.values.get('kwargs')
            if request.values.get('enabled') == 'true':
                enabled = True
            else:
                enabled = False
            every = request.values.get('every')
            period = request.values.get('period')
            minute = request.values.get('minute')
            hour = request.values.get('hour')
            day_of_week = request.values.get('day_of_week')
            day_of_month = request.values.get('day_of_month')
            month_of_year = request.values.get('month_of_year')
            if every and Util.can_tune_to(every, int):
                ret = dict()
                ret['result'] = 1
                SchedulerService.mod_schedule(sid, name, task, args, kwargs, enabled, every=every, period=period)
                return jsonify(ret)
            elif minute or hour or day_of_week or day_of_month or month_of_year:
                ret = dict()
                ret['result'] = 1
                SchedulerService.mod_schedule(sid, name, task, args, kwargs, enabled, minute=minute, hour=hour,
                                              day_of_week=day_of_week, day_of_month=day_of_month,
                                              month_of_year=month_of_year)
                return jsonify(ret)
    return "error", 400


@app.route('/task-config/task', methods=['GET'])
def task_config__task():
    if request.method == 'GET':
        ret = dict()
        ret['result'] = 1
        ts = SchedulerService.get_task_list()
        ret['data'] = ts
        return jsonify(ret)
    return "error", 400


@app.route('/task-his/his', methods=['GET'])
def task_his__his():
    sh_id = request.values.get('id')
    if sh_id:
        if Util.can_tune_to(sh_id, int):
            td = SchedulerService.get_task_history_detail(int(sh_id))
            ret = dict()
            if td:
                ret['result'] = 1
                ret['data'] = td
            else:
                ret['result'] = 2
            return jsonify(ret)
    else:
        query = request.values.get('query', '')
        start_at = Util.check_date_str(request.values.get('startAt'))
        page = request.values.get('p', 1)
        if Util.can_tune_to(page, int):
            pager = SchedulerService.get_task_history(query, start_at).paginate(int(page), perPage, False)
            ret = dict()
            ret['result'] = 1
            his_list = pager.items
            data = dict()
            data['hisList'] = [e.serialize() for e in his_list]
            data['prevNum'] = pager.prev_num
            data['nextNum'] = pager.next_num
            data['total'] = pager.total
            data['perPage'] = perPage
            ret['data'] = data
            return jsonify(ret)
    return "error", 400



