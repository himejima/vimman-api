# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from helpers.crossdomain import crossdomain
from models.model import *  # NOQA

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

app = Blueprint(__name__, "users")


# TODO ログイン方法 dbから検索して照合
# TODO ログイン成功時に 取得データをセッションに入れる
@app.route('/login', methods=['GET', 'POST'])
@crossdomain(origin='*')
def login():
    if request.method == 'POST':
        if request.form['username'] == 'test' and request.form['password'] == 'pass':
            set_username(request.form['username'])
            session['user_id'] = 1
            return redirect('/#/questions')
        else:
            return redirect('/#/login')
    return jsonify(status_code=200)


@app.route('/logout', methods=['GET'])
@crossdomain(origin='*')
def logout():
    clear_session()
    return redirect('/#/login')


def set_username(username):
    session['username'] = username


def get_username():
    return session.get('username')


def is_login():
    return not not get_username()


def user_check():
    if not is_login():
        logging.debug(is_login())
        abort(401)


def clear_session():
    session.clear()
