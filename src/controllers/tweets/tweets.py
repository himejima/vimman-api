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

app = Blueprint(__name__, 'tweets')


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
        tweet = Tweet(
            id=None,
            type=req['type'],
            tweet_id=req['tweet_id'],
            content=req['content'].encode('utf-8'),
            post_url=req['post_url'],
            created_by=created_by,
            updated_by=created_by,
            created_at=tstr,
            updated_at=tstr
        )
        db_session.add(tweet)
        db_session.flush()
        db_session.commit()
        result = {}
        result['id'] = tweet.id
        result['type'] = tweet.type
        result['tweet_id'] = tweet.tweet_id
        result['post_url'] = tweet.post_url
        result['content'] = tweet.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 400


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    per_page = 20
    try:
        param_id = request.args.get('id', '')
        if isinstance(param_id, str) and not param_id.isdigit():
            param_id = ''

        # 0ならばcursorが指定されていない
        param_cursor = request.args.get('cursor', 0)
        # if isinstance(param_cursor, str) and not param_cursor.isdigit():
        #     param_cursor = 0
        param_cursor = int(param_cursor)

        param_query = request.args.get('q', '')
        param_query = param_query.encode('utf-8')
        tweets = []

        base_query = Tweet.query
        if param_id != '':
            base_query = base_query.filter(Tweet.id == param_id)

        if param_query != '':
            base_query = base_query.filter(Tweet.content.like('%' + param_query + '%'))

        param_cursor = int(param_cursor)
        if param_cursor > 0:
            base_query = base_query.filter(Tweet.id >= param_cursor)
        elif param_cursor < 0:
            base_query = base_query.filter(Tweet.id <= ((-1) * param_cursor))

        base_query = base_query.order_by(Tweet.id.desc()).limit(per_page + 1)

        # res = Tweet.query.all()
        res = (base_query.all())

        for row in res:
            tweets.append(row)
        tweets_dict = ListTweetMapper({'result': tweets}).as_dict()
        result = tweets_dict['result']

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

        cursor = {'prev': prev_cursor, 'next': next_cursor}

        return jsonify(result=result, cursor=cursor), 200
    except:
        logging.error(request)
    return '', 404


@app.route('/<tweet_id>', methods=['GET'])
@crossdomain(origin='*')
def read(tweet_id):
    try:
        tweet = (
            Tweet.query
            .filter(text('id = :tweet_id'))
            .params(tweet_id=tweet_id)
            .first()
        )
        tweet_dict = TweetMapper(tweet).as_dict()
        return jsonify(result=tweet_dict), 200
    except:
        logging.error(request)
    return '', 404
