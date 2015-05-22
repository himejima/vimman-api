drop table if exists operations;
drop table if exists questions;
drop table if exists answers;
drop table if exists informations;
drop table if exists tweets;
drop table if exists responses;

create table operations (
    id integer primary key autoincrement,
    username text,
    password text,
    salt text,
    state integer,
    created_at text,
    updated_at text
);
create table questions (
    id integer primary key autoincrement,
    content text,
    state integer,
    created_by text,
    updated_by text,
    created_at text,
    updated_at text
);
create table answers (
    id integer primary key autoincrement,
    question_id integer,
    content text,
    state integer,
    created_by text,
    updated_by text,
    created_at text,
    updated_at text
);
create table informations (
    id integer primary key autoincrement,
    content text,
    state integer,
    created_by text,
    updated_by text,
    created_at text,
    updated_at text 
);
create table tweets (
    id integer primary key autoincrement,
    type text,
    tweet_id integer,
    content text,
    created_by text,
    updated_by text,
    created_at text,
    updated_at text
);
create table responses (
    id integer primary key autoincrement,
    type text,
    content text,
    state text,
    created_by text,
    updated_by text,
    created_at text,
    updated_at text
);
