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
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

app = Blueprint(__name__, 'responses')


@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    created_by = 0  # TODO: created user
    req = json.loads(request.data)
    try:
        response = Response(
            id=None,
            type=req['type'],
            content=req['content'],
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(response)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = response.id
        result['type'] = response.type
        result['state'] = response.state
        result['content'] = response.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 400


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    try:
        responses = []
        res = Response.query.all()
        for row in res:
            responses.append(row)
        responses_dict = ListResponseMapper({'result': responses}).as_dict()
        result = responses_dict['result']
        return jsonify(result=result), 200
    except:
        logging.error(request)
    return '', 404


@app.route('/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def read(response_id):
    try:
        response = (
            Response.query
            .filter(text('id = :response_id'))
            .params(response_id=response_id)
            .first()
        )
        response_dict = ResponseMapper(response).as_dict()
        return jsonify(result=response_dict), 200
    except:
        logging.error(request)
    return '', 404


@app.route('/<response_id>', methods=['PUT'])
@crossdomain(origin='*')
def update(response_id):
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    updated_by = 0
    try:
        row = db_session.query(Response).get(response_id)
        row.type = req['type']
        row.content = req['content']
        row.state = req['state']
        row.updated_by = updated_by
        row.updated_at = tstr
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = row.id
        result['type'] = row.type
        result['state'] = row.state
        result['content'] = row.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 404


@app.route('/<response_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete(response_id):
    code = 204
    try:
        row = Response.query.get(response_id)
        db_session.delete(row)
        db_session.flush()
        db_session.commit()
        return '', 204
    except:
        logging.error(request)
    return '', 404
