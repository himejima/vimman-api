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
    print 'api.01'
    print request.data
    req = json.loads(request.data)
    print 'api.01-1'
    try:
        print 'api.01-2'
        db_session.begin(subtransactions=True)
        print 'api.02'
        question = Question(
            id=None,
            content=req['content'].encode('utf-8'),
            state=req['state'],
            created_by=created_by,
            updated_by=created_by,
            created_at=created_at,
            updated_at=created_at
        )
        print 'api.03'
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
        print db_session.error
        db_session.rollback()
        logging.error(req)
    return '', 400


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index_questions():
    try:
        questions = []
        res = Question.query.all()
        for row in res:
            questions.append(row)
        questions_dict = ListQuestionMapper({'result': questions}).as_dict()
        result = questions_dict['result']
        return jsonify(result=result), 200
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
