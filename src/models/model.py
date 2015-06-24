# -*- coding: utf-8 -*-
from sqlalchemy import *  # NOQA
from sqlalchemy.orm import *  # NOQA
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime as dt
from mappers.mapper import *  # NOQA
from config.databases import *  # NOQA

db_string = '{type}://{user}:{passwd}@{host}:{port}/{db}'.format(
    type=db_config['type'],
    user=db_config['user'],
    passwd=db_config['passwd'],
    host=db_config['host'],
    port=db_config['port'],
    db=db_config['db']
)

engine = create_engine(db_string, echo=False, isolation_level='READ UNCOMMITTED')
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()


class Operator(Base):
    __tablename__ = 'operators'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    salt = Column(String(50))
    state = Column(Integer)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    def __init__(self, id, username, password, salt, state, created_at, updated_at):
        self.id = id
        self.username = username
        self.password = password
        self.salt = salt
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    answers = relationship('Answer')
    creator = relationship(
        'Operator',
        primaryjoin='Question.created_by==Operator.id',
        foreign_keys='Operator.id'
    )
    updater = relationship(
        'Operator',
        primaryjoin='Question.updated_by==Operator.id',
        foreign_keys='Operator.id'
    )
    def __init__(self, id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    creator = relationship(
        'Operator',
        primaryjoin='Answer.created_by==Operator.id',
        foreign_keys='Operator.id'
    )
    updater = relationship(
        'Operator',
        primaryjoin='Answer.updated_by==Operator.id',
        foreign_keys='Operator.id'
    )
    def __init__(self, id, question_id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.question_id = question_id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at


class Information(Base):
    __tablename__ = 'informations'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    creator = relationship(
        'Operator',
        primaryjoin='Information.created_by==Operator.id',
        foreign_keys='Operator.id'
    )
    updater = relationship(
        'Operator',
        primaryjoin='Information.updated_by==Operator.id',
        foreign_keys='Operator.id'
    )
    def __init__(self, id, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    type = Column(String(10))
    tweet_id = Column(Integer)
    content = Column(String)
    post_url = Column(String)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    creator = relationship(
        'Operator',
        primaryjoin='Tweet.created_by==Operator.id',
        foreign_keys='Operator.id'
    )
    updater = relationship(
        'Operator',
        primaryjoin='Tweet.updated_by==Operator.id',
        foreign_keys='Operator.id'
    )
    def __init__(self, id, type, tweet_id, content, post_url, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.type = type
        self.tweet_id = tweet_id
        self.content = content
        self.post_url = post_url
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at


class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True)
    type = Column(String(10))
    content = Column(String)
    state = Column(Integer)
    created_by = Column(String(50))
    updated_by = Column(String(50))
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now)
    creator = relationship(
        'Operator',
        primaryjoin='Response.created_by==Operator.id',
        foreign_keys='Operator.id'
    )
    updater = relationship(
        'Operator',
        primaryjoin='Response.updated_by==Operator.id',
        foreign_keys='Operator.id'
    )
    def __init__(self, id, type, content, state, created_by, updated_by, created_at, updated_at):
        self.id = id
        self.type = type
        self.content = content
        self.state = state
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
