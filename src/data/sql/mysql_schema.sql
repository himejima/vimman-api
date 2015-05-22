-- Vimmanbot MySQL Schema
-- 

DROP TABLE IF EXISTS operators;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS informations;
DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS responses;

CREATE TABLE operators (
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    salt VARCHAR(50),
    state INTEGER,
    -- deleted TINYINT NOT NULL DEFAULT 0,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE questions (
    id INTEGER NOT NULL AUTO_INCREMENT,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE answers (
    id INTEGER NOT NULL AUTO_INCREMENT,
    question_id INTEGER,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE informations (
    id INTEGER NOT NULL AUTO_INCREMENT,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tweets (
    id INTEGER NOT NULL AUTO_INCREMENT,
    type VARCHAR(10),
    tweet_id INTEGER,
    content TEXT,
    post_url TEXT,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE responses (
    id INTEGER NOT NULL AUTO_INCREMENT,
    type VARCHAR(10),
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);
