# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
from helpers.crossdomain import *
from models.model import *

from datetime import datetime as dt
from config.databases import *
import json

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Blueprint(__name__, 'tweets')

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
        tweet = Tweet(
            id=None,
            type=req['type'],
            tweet_id=req['tweet_id'],
            content=req['content'],
            state=req['state'],
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
        result['state'] = tweet.state
        result['content'] = tweet.content
        return jsonify(result=result), 201
    except:
        logging.error(req)
    return '', 400

@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def index():
    try:
        tweets = []
        res = Tweet.query.all()
        for row in res:
            tweets.append(row)
        tweets_dict = ListTweetMapper({'result': tweets}).as_dict()
        result = tweets_dict['result']
        return jsonify(result=result), 200
    except:
        logging.error(request)
    return '', 404

@app.route('/<tweet_id>', methods=['GET'])
@crossdomain(origin='*')
def read(tweet_id):
    try:
        tweet = (
                Tweet.query
                .filter('id = :tweet_id')
                .params(tweet_id=tweet_id)
                .first()
            )
        tweet_dict = TweetMapper(tweet).as_dict()
        return jsonify(result=tweet_dict), 200
    except:
        logging.error(request)
    return '', 404
