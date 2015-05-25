# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

app = Blueprint(__name__, 'informations')

@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    created_by = 0 # TODO: created user
    req = json.loads(request.data)
    try:
        information = Information(
            id=None,
            content=req['content'].encode('utf-8'),
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(information)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = information.id
        result['state'] = information.state
        result['content'] = information.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 400

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    # per_pageとpageを取得
    # TODO: 数字のみを検索するように修正する
    # per_page = request.args.get('per_page', 20)
    # page = request.args.get('page', 1)
    per_page = 20
    # my_offset = (int(page) - 1) * int(per_page)
    # logging.info(per_page)
    # logging.info(page)
    # logging.info(my_offset)
    param_id = request.args.get('id', '')
    # 0ならばcursorが指定されていない
    param_cursor = request.args.get('cursor', 0)
    param_query = request.args.get('q', '')

    try:
        informations = []
        res = (
                Information.query
                .order_by(Information.id.desc())
                .limit(per_page)
                .all()
            )

        for row in res:
            informations.append(row)
        informations_dict = ListInformationMapper({'result': informations}).as_dict()
        result = informations_dict['result']

        # 空でなければ
        logging.info(result[-1]['id'])
        prev_cursor = (-1) * result[-1]['id']
        next_cursor = result[0]['id']

        cursor = { 'prev' : prev_cursor, 'next' : next_cursor }
        
        return jsonify(result=result, cursor=cursor), 200
    except:
        logging.error(request)
    return '', 404

@app.route('/<information_id>', methods=['GET'])
@crossdomain(origin='*')
def read(information_id):
    try:
        information = (
                Information.query
                .filter('id = :information_id')
                .params(information_id=information_id)
                .first()
            )
        information_dict = InformationMapper(information).as_dict()
        return jsonify(result=information_dict), 200
    except:
        logging.error(request)
    return '', 404

@app.route('/<information_id>', methods=['PUT'])
@crossdomain(origin='*')
def update(information_id):
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    tstr = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    req = json.loads(request.data)
    updated_by = 0
    try:
        row = db_session.query(Information).get(information_id)
        row.content = req['content']
        row.state = req['state']
        row.updated_by = updated_by
        row.updated_at = tstr
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = row.id
        result['state'] = row.state
        result['content'] = row.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 404

@app.route('/<information_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete(information_id):
    try:
        row = Information.query.get(information_id)
        db_session.delete(row)
        db_session.flush()
        db_session.commit()
        return '', 204
    except:
        logging.error(request)
    return '', 404
