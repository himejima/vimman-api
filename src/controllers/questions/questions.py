# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
from flask import request
from helpers.crossdomain import crossdomain
from models.model import *  # NOQA
from datetime import datetime as dt
import json
import logging
LOG_FILENAME = 'questions.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %p %I:%M:%S'
)

app = Blueprint(__name__, 'questions')


# TODO: パラメータ不足時のエラー処理
@app.route('/', methods=['POST'])
@crossdomain(origin='*')
def create():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    created_at = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    created_by = 0  # TODO: created user
    req = json.loads(request.data)
    try:
        db_session.begin(subtransactions=True)
        question = Question(
            id=None,
            content=req['content'].encode('utf-8'),
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=created_at,
            updated_at=created_at
        )
        db_session.add(question)
        db_session.flush()
        answers = req['answers'].split('\r\n')
        for answer_text in answers:
            answer = Answer(
                id=None,
                question_id=question.id,
                content=answer_text,
                state=1,
                created_by=created_by,
                updated_by=created_by,
                created_at=created_at,
                updated_at=created_at
            )
            db_session.add(answer)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = question.id
        result['state'] = question.state
        result['content'] = question.content
        return jsonify(result=result), 201
    except:
        db_session.rollback()
        db_session.close()
        logging.error(req)
    return '', 400


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_questions():
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
        questions = []
        base_query = Question.query
        if param_id != '':
            base_query = base_query.filter(Question.id == param_id)

        if param_query != '':
            base_query = base_query.filter(Question.content.like('%' + param_query + '%'))

        param_cursor = int(param_cursor)
        if param_cursor > 0:
            base_query = base_query.filter(Question.id >= param_cursor)
        elif param_cursor < 0:
            base_query = base_query.filter(Question.id <= ((-1) * param_cursor))

        base_query = base_query.order_by(Question.id.desc()).limit(per_page + 1)
        #res = Question.query.all()
        res = (base_query.all())

        for row in res:
            questions.append(row)
        questions_dict = ListQuestionMapper({'result': questions}).as_dict()
        result = questions_dict['result']

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


@app.route('/<question_id>', methods=['GET'])
@crossdomain(origin='*')
def show_question(question_id):
    try:
        question = (
            Question.query
            .filter(text('id = :question_id'))
            .params(question_id=question_id)
            .first()
        )
        question_dict = QuestionMapper(question).as_dict()
        return jsonify(result=question_dict), 200
    except:
        logging.error(request)
    return '', 404


# TODO: パラメータ不足時のエラー処理
@app.route('/<question_id>', methods=['PUT'])
@crossdomain(origin='*')
def edit_question(question_id):
    if request.headers['Content-Type'] != 'application/json':
        return jsonify(message='error'), 400
    tdatetime = dt.now()
    updated_at = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
    updated_by = 0  # TODO: updated user
    req = json.loads(request.data)
    try:
        db_session.begin(subtransactions=True)
        question = db_session.query(Question).get(question_id)
        question.content = req['content']
        question.state = req['state']
        question.updated_by = updated_by
        question.updated_at = updated_at
        answer_texts = req['answers'].split('\r\n')
        res_answers = Answer.query.filter(Answer.question_id == question_id).all()
        for res_answer in res_answers:
            db_session.delete(res_answer)
        db_session.flush()
        db_session.commit()
        for answer_text in answer_texts:
            answer = Answer(
                id=None,
                question_id=question_id,
                content=answer_text,
                state=1,
                created_by=updated_by,
                updated_by=updated_by,
                created_at=updated_at,
                updated_at=updated_at
            )
            db_session.add(answer)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = question.id
        result['state'] = question.state
        result['content'] = question.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
        db_session.rollback()
    return '', 400


@app.route('/<question_id>', methods=['DELETE'])
@crossdomain(origin='*')
def delete_question(question_id):
    try:
        answers = Answer.query.filter(Answer.question_id == question_id).all()
        for answer in answers:
            db_session.delete(answer)
        question = Question.query.get(question_id)
        db_session.delete(question)
        db_session.flush()
        db_session.commit()
        return '', 204
    except:
        logging.error(request)
    return '', 404
