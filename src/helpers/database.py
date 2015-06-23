# -*- coding: utf-8 -*-
u""" Database Helpers
"""
from contextlib import closing
import sqlite3


def connect_db(database):
    return sqlite3.connect(database)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
