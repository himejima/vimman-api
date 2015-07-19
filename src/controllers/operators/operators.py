# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
from flask import request
from helpers.crossdomain import crossdomain
from models.model import *  # NOQA
from datetime import datetime as dt
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

app = Blueprint(__name__, 'operators')


@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    try:
        operator = Operator(
            id=None,
            username=req['username'].encode('utf-8'),
            password=req['password'],
            salt='salt1',
            state=req['state'],
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(operator)
        db_session.commit()
        result = {}
        result['id'] = operator.id
        result['username'] = operator.username
        result['state'] = operator.state
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 400


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    per_page = 20
    param_id = request.args.get('id', '')
    if isinstance(param_id, str) and not param_id.isdigit():
        param_id = ''

    # 0ならばcursorが指定されていない
    param_cursor = request.args.get('cursor', 0)
    if isinstance(param_cursor, str) and not param_cursor.isdigit():
        param_cursor = 0

    param_query = request.args.get('q', '')
    param_query = param_query.encode('utf-8')

    try:
        #operators = get_operators()
        operators = []
        base_query = Operator.query
        if param_id != '':
            base_query = base_query.filter(Operator.id == param_id)

        if param_query != '':
            base_query = base_query.filter(Operator.username.like('%' + param_query + '%'))

        param_cursor = int(param_cursor)
        if param_cursor > 0:
            base_query = base_query.filter(Operator.id >= param_cursor)
        elif param_cursor < 0:
            base_query = base_query.filter(Operator.id <= ((-1) * param_cursor))

        base_query = base_query.order_by(Operator.id.desc()).limit(per_page + 1)
        res = (base_query.all())

        #res = Operator.query.all()
        for row in res:
            operators.append(row)

        operators_dict = ListOperatorMapper({'result': operators}).as_dict()
        result = operators_dict['result']

        prev_cursor = 0
        next_cursor = 0

        if len(result) == (per_page + 1):
            prev_cursor = (-1) * result[-1]['id']
            next_cursor = result[0]['id']
        elif len(result) > 0:
            if param_cursor > 0:
                prev_cursor = (-1) * result[-1]['id']
            elif param_cursor < 0:
                next_cursor = result[0]['id']

        cursor = { 'prev' : prev_cursor, 'next' : next_cursor }

        return jsonify(result=result, cursor=cursor), 200
    except:
        logging.error(request)
    return '', 404


@app.route('/<operator_id>', methods=['GET'])
@crossdomain(origin='*')
def read(operator_id):
    operator_dict = {}
    try:
        operator = get_operator(operator_id)
        operator_dict = OperatorMapper(operator).as_dict()
        return jsonify(result=operator_dict), 200
    except:
        logging.error(request)
    return '', 404


def get_operator(operator_id):
    operator = None
    operator = Operator.query.filter(text("id = :operator_id")).params(operator_id=operator_id).first()
    return operator


#def get_operators():
#    operators = []
#    res = Operator.query.all()
#    for row in res:
#        operators.append(row)
#    return operators


@app.route('/<operator_id>', methods=['PUT'])
@crossdomain(origin='*')
def update(operator_id):
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    result = {}
    try:
        row = db_session.query(Operator).get(operator_id)
        row.username = req['username']
        row.password = req['password']
        row.state = req['state']
        row.updated_at = tstr
        db_session.flush()
        db_session.commit()
        result['id'] = row.id
        result['username'] = row.username
        result['state'] = row.state
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 404


@app.route('/<operator_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete(operator_id):
    try:
        row = Operator.query.get(operator_id)
        db_session.delete(row)
        db_session.flush()
        db_session.commit()
        return '', 204
    except:
        logging.error(request)
    return '', 404


def delete_all():
    try:
        Operator.query.delete()
    except:
        logging.error(request)
