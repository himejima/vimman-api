# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
from flask import session
from flask import request
from helpers.crossdomain import crossdomain
from models.model import *  # NOQA
from datetime import datetime as dt

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

app = Blueprint(__name__, 'responses')


@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def add_response():
    code = 201
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = request.form
    creator_id = 0
    if session.get('user_id') is not None:
        creator_id = session.get('user_id')
    try:
        response = Response(
            id=None,
            type=req['responses[type]'],
            content=req['responses[content]'],
            state=req['responses[state]'],
            created_by=creator_id,
            updated_by=creator_id,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(response)
        db_session.commit()
    except:
        pass
    finally:
        pass
    return jsonify(status_code=code)


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_responses():
    code = 200
    try:
        responses = get_responses()
        responses_dict = ListResponseMapper({'result': responses}).as_dict()
    except:
        pass
    result = responses_dict['result']
    return jsonify(status_code=code, result=result)


@app.route('/<response_id>', methods=['GET'])
@crossdomain(origin='*')
def show_response(response_id):
    try:
        response = (
            Response.query
            .filter('id = :response_id')
            .params(response_id=response_id)
            .first()
        )
        response_dict = ResponseMapper(response).as_dict()
        return jsonify(result=information_dict), 200
    except:
        logging.error(request)
    return '', 404


def get_response(response_id):
    response = []
    response = Response.query.filter('id = :response_id').params(response_id=response_id).first()
    return response


def get_responses():
    responses = []
    res = Response.query.all()
    for row in res:
        responses.append(row)
    return responses


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
