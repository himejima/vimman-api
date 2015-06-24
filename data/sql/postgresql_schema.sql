-- Vimmanbot MySQL Schema
-- 

DROP TABLE IF EXISTS operators;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS informations;
DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS responses;

CREATE TABLE operators (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    salt VARCHAR(50),
    state INTEGER,
    -- deleted TINYINT NOT NULL DEFAULT 0,
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE informations (
    id SERIAL PRIMARY KEY,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE tweets (
    id SERIAL PRIMARY KEY,
    type VARCHAR(10),
    tweet_id INTEGER,
    content TEXT,
    post_url TEXT,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    type VARCHAR(10),
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at timestamp NOT NULL,
    updated_at timestamp NOT NULL
);
